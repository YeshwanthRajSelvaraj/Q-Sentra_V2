"""
Q-Sentra Discovery Route
API Endpoints: POST /api/discovery/start, GET /api/discovery/results, POST /api/discovery/confirm/{id}, POST /api/discovery/ignore/{id}
"""
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from core.database import get_db
from models.domain import DiscoveryQueue, Asset
from services.discovery.discovery_engine import DiscoveryEngine

router = APIRouter(prefix="/api/discovery", tags=["Discovery"])

class DiscoverRequest(BaseModel):
    scope: str
    options: dict

async def run_discovery_task(scope: str, options: dict, db: AsyncSession):
    engine = DiscoveryEngine(options)
    domains = ["pnb.co.in", "pnb.bank.in"] if "PNB" in scope else [scope]
    
    results = []
    for d in domains:
        res = await engine.discover(d)
        results.extend(res)
        
    for r in results:
        stmt = select(DiscoveryQueue).where(DiscoveryQueue.hostname == r["hostname"])
        exist_res = await db.execute(stmt)
        if not exist_res.scalars().first():
            db.add(DiscoveryQueue(
                hostname=r["hostname"],
                ip_address=r.get("ip_address"),
                source=r.get("source", "DNS"),
                status="PENDING"
            ))
    
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"Failed to commit discovery results: {e}")

@router.post("/start")
async def start_discovery(req: DiscoverRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    background_tasks.add_task(run_discovery_task, req.scope, req.options, db)
    return {"status": "Discovery started successfully", "scope": req.scope}

@router.get("/results")
async def get_discovery_results(db: AsyncSession = Depends(get_db)):
    stmt = select(DiscoveryQueue).order_by(DiscoveryQueue.first_seen.desc())
    res = await db.execute(stmt)
    records = res.scalars().all()
    return records

@router.post("/confirm/{asset_id}")
async def confirm_discovery(asset_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(DiscoveryQueue).where(DiscoveryQueue.id == asset_id)
    res = await db.execute(stmt)
    q = res.scalars().first()
    if not q: 
        raise HTTPException(status_code=404, detail="Not found")
    
    q.status = "CONFIRMED"
    
    asset = Asset(
        hostname=q.hostname,
        ip_address=q.ip_address,
        asset_type="domain",
        status="confirmed"
    )
    db.add(asset)
    await db.commit()
    return {"status": "Confirmed"}

@router.post("/ignore/{asset_id}")
async def ignore_discovery(asset_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(DiscoveryQueue).where(DiscoveryQueue.id == asset_id)
    res = await db.execute(stmt)
    q = res.scalars().first()
    if not q: 
        raise HTTPException(status_code=404, detail="Not found")
    
    q.status = "IGNORED"
    await db.commit()
    return {"status": "Ignored"}
