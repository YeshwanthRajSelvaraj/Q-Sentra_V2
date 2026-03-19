"""
Q-Sentra: Quantum-Proof Cryptographic Asset Management Platform
Punjab National Bank - CyberSecurity Hackathon 2026

Main FastAPI Application Entry Point
"""

import os
import json
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from core.database import init_db, close_db
from core.websocket_manager import ws_manager
from routes import (
    auth_router,
    assets_router,
    scans_router,
    cbom_router,
    pqc_router,
    risk_router,
    remediation_router,
    certificates_router,
    dashboard_router,
    discovery_router,
    verify_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    print("🚀 Q-Sentra starting up...")
    await init_db()
    print("✅ Database connections established")
    print("🛡️  Q-Sentra is ready to protect PNB's cryptographic infrastructure")
    yield
    await close_db()
    print("🔒 Q-Sentra shutdown complete")


app = FastAPI(
    title="Q-Sentra API",
    description=(
        "Quantum-Proof Cryptographic Asset Management Platform for Punjab National Bank. "
        "Autonomous AI-driven cryptographic discovery, validation, and quantum-readiness orchestration."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "PNB Cybersecurity Team",
        "email": "cybersecurity@pnb.co.in",
    },
    license_info={
        "name": "Proprietary - Punjab National Bank",
    },
)

# ─── CORS Middleware ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── API Routes ────────────────────────────────────────────────────
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(assets_router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(scans_router, prefix="/api/v1/scans", tags=["Scans"])
app.include_router(cbom_router, prefix="/api/v1/cbom", tags=["CBOM"])
app.include_router(pqc_router, prefix="/api/v1/pqc", tags=["PQC Validation"])
app.include_router(risk_router, prefix="/api/v1/risk", tags=["Risk Analysis"])
app.include_router(remediation_router, prefix="/api/v1/remediation", tags=["Remediation"])
app.include_router(certificates_router, prefix="/api/v1/certificates", tags=["Certificates"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(discovery_router, prefix="/api/v1/discovery", tags=["Discovery"])
app.include_router(verify_router, prefix="/api/v1/verify", tags=["Public Verification"])


# ─── WebSocket Endpoint ───────────────────────────────────────────
@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time updates via WebSocket."""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong", "timestamp": datetime.utcnow().isoformat()}))
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# ─── Health Check ──────────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "Q-Sentra API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "organization": "Punjab National Bank",
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint."""
    return {
        "name": "Q-Sentra",
        "tagline": "Quantum-Proof Cryptographic Asset Management",
        "organization": "Punjab National Bank",
        "version": "1.0.0",
        "docs": "/api/docs",
    }
