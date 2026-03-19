"""
Q-Sentra Dashboard Route
Provides aggregated data for the real-time dashboard.
"""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from core.security import get_current_user
from core.websocket import ws_manager
from engines.scanner import CryptoScanner
from engines.pqc_validator import PQCValidator

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/metrics")
async def dashboard_overview(user: dict = Depends(get_current_user)):
    """Get dashboard overview KPIs."""
    # Scan a sample of PNB domains
    scanner = CryptoScanner()
    validator = PQCValidator()
    domains = [
        "www.pnb.co.in", "netbanking.pnb.co.in", "api.pnb.co.in",
        "mobile.pnb.co.in", "vpn.pnb.co.in", "upi.pnb.co.in",
    ]

    results = []
    for domain in domains:
        scan = await scanner.scan(domain)
        pqc = validator.validate(scan)
        results.append({
            "host": domain,
            "quantum_score": pqc["quantum_score"],
            "risk_category": pqc["risk_category"],
            "tls_version": scan.get("tls_version", "Unknown"),
            "key_exchange": scan.get("key_exchange", "Unknown"),
            "vulnerabilities": len(scan.get("vulnerabilities", [])),
        })

    scores = [r["quantum_score"] for r in results]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    return {
        "total_assets": len(results),
        "avg_pqc_score": avg_score,
        "at_risk_count": sum(1 for s in scores if s < 60),
        "pqc_ready_count": sum(1 for s in scores if s >= 90),
        "moderate_assets": sum(1 for s in scores if 60 <= s < 90),
        "assets": results,
        "active_websockets": ws_manager.active_connections,
    }


@router.get("/recent-activity")
async def recent_activity(user: dict = Depends(get_current_user)):
    return [
        {"id": 1, "message": "High-risk asset vpn.pnb.co.in detected with RSA-2048", "severity": "danger", "time": "2 mins ago"},
        {"id": 2, "message": "PQC Assessment completed for netbanking.pnb.co.in", "severity": "success", "time": "15 mins ago"},
        {"id": 3, "message": "New expired certificate logged for demo-server", "severity": "warning", "time": "1 hour ago"},
        {"id": 4, "message": "API gateway updated to purely TLS 1.3", "severity": "info", "time": "3 hours ago"},
    ]


@router.get("/geodistribution")
async def geo_distribution(user: dict = Depends(get_current_user)):
    return []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time dashboard updates."""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or process commands
            await websocket.send_json({
                "type": "ack",
                "message": f"Received: {data}",
                "active_connections": ws_manager.active_connections,
            })
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
