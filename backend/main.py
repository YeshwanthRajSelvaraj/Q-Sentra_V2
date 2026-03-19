"""
Q-Sentra – Quantum-Safe Cryptographic Asset Management Platform
Main FastAPI Application

Production-grade API server with:
  - 8 mandatory endpoints (/discover, /scan, /cbom, /score, /risk, /remediate, /certificate, /verify)
  - JWT authentication + RBAC (Admin, Analyst, DevOps)
  - WebSocket real-time updates
  - Input validation via Pydantic
  - CORS + security headers
"""
import logging
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import get_settings
from routes import auth, discover, scan, cbom, score, risk, remediate, certificate, dashboard, rating

# ── Logging Configuration ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("qsentra.main")

settings = get_settings()


# ── Lifespan Events ──
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("=" * 60)
    logger.info("  Q-Sentra Platform Starting...")
    logger.info(f"  Version: {settings.APP_VERSION}")
    logger.info(f"  Debug: {settings.DEBUG}")
    logger.info(f"  Demo Mode: {settings.DEMO_MODE}")
    logger.info("=" * 60)

    # Initialize databases (optional - works without them in demo mode)
    try:
        from core.database import init_postgres, init_mongo
        await init_postgres()
        await init_mongo()
        logger.info("✓ Databases connected")
    except Exception as e:
        logger.warning(f"⚠ Database connection skipped (demo mode): {e}")

    yield

    # Shutdown
    logger.info("Q-Sentra shutting down...")
    try:
        from core.database import close_databases
        await close_databases()
    except Exception:
        pass


# ── FastAPI App ──
app = FastAPI(
    title="Q-Sentra API",
    description=(
        "Quantum-Safe Cryptographic Asset Management Platform for Punjab National Bank. "
        "Discovers, scans, validates, and remediates cryptographic assets against "
        "NIST Post-Quantum Cryptography standards (FIPS 203/204/205)."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Security Headers Middleware ──
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# ── Register Routes ──
app.include_router(auth.router)
app.include_router(discover.router)
app.include_router(scan.router)
app.include_router(cbom.router)
app.include_router(score.router)
app.include_router(risk.router)
app.include_router(remediate.router)
app.include_router(certificate.router)
app.include_router(dashboard.router)
app.include_router(rating.router)


# ── Health Check ──
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - system status."""
    return {
        "service": "Q-Sentra API",
        "version": settings.APP_VERSION,
        "status": "operational",
        "description": "Quantum-Safe Cryptographic Asset Management Platform",
        "endpoints": {
            "docs": "/docs",
            "discover": "POST /discover",
            "scan": "GET/POST /scan/{asset}",
            "cbom": "GET /cbom/{asset}",
            "score": "GET /score/{asset}",
            "risk": "GET /risk/{asset}",
            "remediate": "GET /remediate/{asset}",
            "certificate": "GET /certificate/{asset}",
            "verify": "GET /verify/{cert_id}",
            "dashboard": "GET /dashboard/overview",
            "websocket": "WS /ws",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    health = {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "components": {
            "api": "up",
            "demo_mode": settings.DEMO_MODE,
        },
    }

    # Check databases
    try:
        from core.database import get_mongo
        db = get_mongo()
        await db.command("ping")
        health["components"]["mongodb"] = "up"
    except Exception:
        health["components"]["mongodb"] = "unavailable (demo mode)"

    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        health["components"]["redis"] = "up"
        await r.close()
    except Exception:
        health["components"]["redis"] = "unavailable (demo mode)"

    return health


# ── Global Exception Handler ──
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
        },
    )
