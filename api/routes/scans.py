"""Scan management routes."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import uuid

router = APIRouter()


class ScanRequest(BaseModel):
    assetId: str
    scanType: str = "full"


class BatchScanRequest(BaseModel):
    assetIds: list[str]
    scanType: str = "full"


SCAN_HISTORY = [
    {
        "scanId": "scan-20260310-001", "assetId": "web01.pnb.co.in",
        "scanType": "full", "status": "completed",
        "startedAt": "2026-03-10T14:30:00Z", "completedAt": "2026-03-10T14:30:45Z",
        "durationMs": 45200,
        "results": {
            "tlsVersion": "1.2", "cipherSuite": "TLS_RSA_WITH_AES_128_CBC_SHA",
            "keyExchange": "RSA", "quantumScore": 15,
            "vulnerabilities": ["RSA key exchange vulnerable to Shor's algorithm", "TLS 1.2 lacks PQC support"],
        },
    },
    {
        "scanId": "scan-20260310-002", "assetId": "netbanking.pnb.co.in",
        "scanType": "full", "status": "completed",
        "startedAt": "2026-03-10T14:35:00Z", "completedAt": "2026-03-10T14:35:38Z",
        "durationMs": 38100,
        "results": {
            "tlsVersion": "1.2", "cipherSuite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "keyExchange": "ECDHE", "quantumScore": 25,
            "vulnerabilities": ["ECDHE vulnerable to quantum key recovery", "RSA signatures at risk"],
        },
    },
    {
        "scanId": "scan-20260310-003", "assetId": "swift.pnb.co.in",
        "scanType": "full", "status": "completed",
        "startedAt": "2026-03-10T15:10:00Z", "completedAt": "2026-03-10T15:10:22Z",
        "durationMs": 22400,
        "results": {
            "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384",
            "keyExchange": "ML-KEM-768", "quantumScore": 95,
            "vulnerabilities": [],
        },
    },
]


@router.post("", status_code=202)
async def initiate_scan(request: ScanRequest):
    """Initiate a new cryptographic scan."""
    scan_id = f"scan-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    return {
        "scanId": scan_id,
        "assetId": request.assetId,
        "scanType": request.scanType,
        "status": "queued",
        "estimatedCompletion": (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z",
        "message": f"Scan queued for {request.assetId}",
    }


@router.post("/batch", status_code=202)
async def initiate_batch_scan(request: BatchScanRequest):
    """Initiate batch scan for multiple assets."""
    scans = []
    for asset_id in request.assetIds:
        scan_id = f"scan-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        scans.append({
            "scanId": scan_id,
            "assetId": asset_id,
            "status": "queued",
        })
    return {
        "batchId": f"batch-{uuid.uuid4().hex[:8]}",
        "totalScans": len(scans),
        "scans": scans,
        "estimatedCompletion": (datetime.utcnow() + timedelta(minutes=15)).isoformat() + "Z",
    }


@router.get("")
async def list_scans(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
):
    """List scan history."""
    filtered = SCAN_HISTORY.copy()
    if status:
        filtered = [s for s in filtered if s["status"] == status]

    return {
        "data": filtered,
        "pagination": {"page": page, "limit": limit, "total": len(filtered)},
    }


@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    """Get scan details."""
    scan = next((s for s in SCAN_HISTORY if s["scanId"] == scan_id), None)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan
