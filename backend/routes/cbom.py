"""
Q-Sentra CBOM Routes
GET /api/cbom/{hostname}
POST /api/cbom/refresh/{hostname}
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from core.database import get_db
from models.domain import CBOM, Asset
from services.scanner.tls_scanner import TLSScanner

router = APIRouter(prefix="/api/cbom", tags=["CBOM"])

@router.get("/{hostname}")
async def get_cbom(hostname: str, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    stmt = select(CBOM).where(CBOM.hostname == hostname).order_by(CBOM.scan_timestamp.desc())
    result = await db.execute(stmt)
    cbom = result.scalars().first()
    
    if cbom:
        return cbom.cbom_data

    # If it doesn't exist, trigger scan
    return await scan_and_save_cbom(hostname, db)

@router.post("/refresh/{hostname}")
async def refresh_cbom(hostname: str, db: AsyncSession = Depends(get_db)):
    return await scan_and_save_cbom(hostname, db)

async def scan_and_save_cbom(hostname: str, db: AsyncSession):
    scanner = TLSScanner(hostname)
    scan_result = scanner.scan()
    
    if "error" in scan_result:
        raise HTTPException(status_code=400, detail=scan_result["error"])

    # Attempt to link to an existing asset
    stmt = select(Asset).where(Asset.hostname == hostname)
    result = await db.execute(stmt)
    asset = result.scalars().first()
    
    new_cbom = CBOM(
        hostname=hostname,
        cbom_data=scan_result,
        asset_id=asset.id if asset else None
    )
    db.add(new_cbom)
    await db.commit()
    
    return scan_result
