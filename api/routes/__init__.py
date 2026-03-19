"""Q-Sentra API Routes."""

from routes.auth import router as auth_router
from routes.assets import router as assets_router
from routes.scans import router as scans_router
from routes.cbom import router as cbom_router
from routes.pqc import router as pqc_router
from routes.risk import router as risk_router
from routes.remediation import router as remediation_router
from routes.certificates import router as certificates_router
from routes.dashboard import router as dashboard_router
from routes.discovery import router as discovery_router
from routes.verify import router as verify_router

__all__ = [
    "auth_router",
    "assets_router",
    "scans_router",
    "cbom_router",
    "pqc_router",
    "risk_router",
    "remediation_router",
    "certificates_router",
    "dashboard_router",
    "discovery_router",
    "verify_router",
]
