"""
Q-Sentra PQC Score Routes
GET /api/pqc-score/{hostname}
GET /api/pqc-score/batch
GET /api/pqc-score/explain/{hostname}
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from core.database import get_db
from models.domain import PQCScore, CBOM, Asset
from ml.pqc_scorer import PQCScorer

router = APIRouter(prefix="/api/pqc-score", tags=["PQC Score"])
scorer = PQCScorer()

@router.get("/batch")
async def batch_score(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    background_tasks.add_task(batch_score_all, db)
    return {"status": "Batch scoring initiated."}

@router.get("/{hostname}")
async def get_pqc_score(hostname: str, db: AsyncSession = Depends(get_db)):
    stmt = select(PQCScore).join(Asset).where(Asset.hostname == hostname).order_by(PQCScore.scanned_at.desc())
    result = await db.execute(stmt)
    score_record = result.scalars().first()
    
    if score_record:
        return {
            "score": score_record.score,
            "confidence": score_record.confidence,
            "model_version": score_record.model_version,
            "explanations": score_record.shap_explanation
        }
        
    stmt = select(CBOM).where(CBOM.hostname == hostname).order_by(CBOM.scan_timestamp.desc())
    result = await db.execute(stmt)
    cbom = result.scalars().first()
    
    cv = cbom.cbom_data if cbom else {}
    score_res = scorer.score(cv)
    
    stmt = select(Asset).where(Asset.hostname == hostname)
    result = await db.execute(stmt)
    asset = result.scalars().first()
    
    if asset:
        new_score = PQCScore(
            asset_id=asset.id,
            score=score_res["score"],
            confidence=score_res["confidence"],
            shap_explanation=score_res.get("explanations", []),
            model_version=score_res["model_version"]
        )
        db.add(new_score)
        await db.commit()

    return score_res

@router.get("/explain/{hostname}")
async def explain_pqc_score(hostname: str, db: AsyncSession = Depends(get_db)):
    score_data = await get_pqc_score(hostname, db)
    return {"explanations": score_data.get("explanations", [])}

async def batch_score_all(db: AsyncSession):
    stmt = select(Asset)
    result = await db.execute(stmt)
    assets = result.scalars().all()
    for a in assets:
        stmt_cbom = select(CBOM).where(CBOM.hostname == a.hostname).order_by(CBOM.scan_timestamp.desc())
        res = await db.execute(stmt_cbom)
        cbom = res.scalars().first()
        cv = cbom.cbom_data if cbom else {}
        score_res = scorer.score(cv)
        
        new_score = PQCScore(
            asset_id=a.id,
            score=score_res["score"],
            confidence=score_res["confidence"],
            shap_explanation=score_res.get("explanations", []),
            model_version=score_res["model_version"]
        )
        db.add(new_score)
    
    await db.commit()
