"""
Q-Sentra Scan Route
POST/GET /scan/{asset} - Scan cryptographic configuration of an asset.
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from core.security import get_current_user
from core.websocket import ws_manager
from engines.scanner import CryptoScanner

router = APIRouter(tags=["Scanner"])

# Scan result cache (use MongoDB in production)
_scan_cache = {}


class ScanRequest(BaseModel):
    port: int = 443
    force_rescan: bool = False


@router.post("/scan/{asset}")
async def scan_asset(asset: str, req: ScanRequest = ScanRequest(),
                     bg: BackgroundTasks = None,
                     user: dict = Depends(get_current_user)):
    """
    Scan an asset's TLS/cryptographic configuration.
    Uses Python's ssl module for real TLS handshake analysis.
    """
    # Check cache unless force rescan
    if not req.force_rescan and asset in _scan_cache:
        return {"source": "cache", "result": _scan_cache[asset]}

    scanner = CryptoScanner()

    # Notify scan start
    if bg:
        bg.add_task(ws_manager.send_scan_update, asset, "scanning")

    result = await scanner.scan(asset, req.port)
    _scan_cache[asset] = result

    # Notify scan complete
    if bg:
        bg.add_task(ws_manager.send_scan_update, asset, "complete", {
            "tls_version": result.get("tls_version"),
            "cipher_suite": result.get("cipher_suite"),
            "vulnerabilities_count": len(result.get("vulnerabilities", [])),
        })

    return {"source": "live_scan", "result": result}


@router.get("/scan/{asset}")
async def get_scan_result(asset: str, user: dict = Depends(get_current_user)):
    """Get cached scan result for an asset, or run a new scan."""
    if asset in _scan_cache:
        return {"source": "cache", "result": _scan_cache[asset]}

    scanner = CryptoScanner()
    result = await scanner.scan(asset)
    _scan_cache[asset] = result
    return {"source": "live_scan", "result": result}
