"""Asset management routes."""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ─── Mock Data ─────────────────────────────────────────────────────
ASSETS = [
    {
        "id": "1", "assetId": "web01.pnb.co.in", "domain": "web01.pnb.co.in",
        "ip": "203.123.45.67", "port": 443, "assetType": "web",
        "tlsVersion": "1.2", "cipherSuite": "TLS_RSA_WITH_AES_128_CBC_SHA",
        "keyExchange": "RSA", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048,
        "certificate": {"issuer": "DigiCert", "expiry": "2026-12-31T23:59:59Z", "serial": "0A:1B:2C:3D"},
        "quantumScore": 15, "status": "critical", "isPublic": True,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T14:30:00Z", "discoveredAt": "2026-01-15T10:00:00Z",
    },
    {
        "id": "2", "assetId": "netbanking.pnb.co.in", "domain": "netbanking.pnb.co.in",
        "ip": "203.123.45.68", "port": 443, "assetType": "web",
        "tlsVersion": "1.2", "cipherSuite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "keyExchange": "ECDHE", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048,
        "certificate": {"issuer": "DigiCert", "expiry": "2026-09-15T23:59:59Z", "serial": "1B:2C:3D:4E"},
        "quantumScore": 25, "status": "critical", "isPublic": True,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T14:35:00Z", "discoveredAt": "2026-01-15T10:05:00Z",
    },
    {
        "id": "3", "assetId": "api.pnb.co.in", "domain": "api.pnb.co.in",
        "ip": "203.123.45.69", "port": 443, "assetType": "api",
        "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384",
        "keyExchange": "X25519", "signatureAlgorithm": "ECDSA-SHA384", "keySize": 384,
        "certificate": {"issuer": "Let's Encrypt", "expiry": "2026-06-30T23:59:59Z", "serial": "2C:3D:4E:5F"},
        "quantumScore": 45, "status": "warning", "isPublic": True,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T14:40:00Z", "discoveredAt": "2026-01-20T08:00:00Z",
    },
    {
        "id": "4", "assetId": "mobile.pnb.co.in", "domain": "mobile.pnb.co.in",
        "ip": "203.123.45.70", "port": 443, "assetType": "mobile_api",
        "tlsVersion": "1.3", "cipherSuite": "TLS_AES_128_GCM_SHA256",
        "keyExchange": "X25519", "signatureAlgorithm": "ECDSA-SHA256", "keySize": 256,
        "certificate": {"issuer": "DigiCert", "expiry": "2027-03-31T23:59:59Z", "serial": "3D:4E:5F:6G"},
        "quantumScore": 40, "status": "warning", "isPublic": True,
        "latitude": 19.0760, "longitude": 72.8777,
        "lastScanAt": "2026-03-10T14:45:00Z", "discoveredAt": "2026-01-20T08:05:00Z",
    },
    {
        "id": "5", "assetId": "vpn.pnb.co.in", "domain": "vpn.pnb.co.in",
        "ip": "203.123.45.71", "port": 443, "assetType": "vpn",
        "tlsVersion": "1.2", "cipherSuite": "TLS_RSA_WITH_AES_256_CBC_SHA256",
        "keyExchange": "RSA", "signatureAlgorithm": "RSA-SHA256", "keySize": 4096,
        "certificate": {"issuer": "Internal CA", "expiry": "2027-06-30T23:59:59Z", "serial": "4E:5F:6G:7H"},
        "quantumScore": 20, "status": "critical", "isPublic": False,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T14:50:00Z", "discoveredAt": "2026-02-01T12:00:00Z",
    },
    {
        "id": "6", "assetId": "mail.pnb.co.in", "domain": "mail.pnb.co.in",
        "ip": "203.123.45.72", "port": 443, "assetType": "email",
        "tlsVersion": "1.2", "cipherSuite": "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "keyExchange": "ECDHE", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048,
        "certificate": {"issuer": "GlobalSign", "expiry": "2026-11-30T23:59:59Z", "serial": "5F:6G:7H:8I"},
        "quantumScore": 30, "status": "warning", "isPublic": True,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T14:55:00Z", "discoveredAt": "2026-02-01T12:05:00Z",
    },
    {
        "id": "7", "assetId": "upi.pnb.co.in", "domain": "upi.pnb.co.in",
        "ip": "203.123.45.73", "port": 443, "assetType": "payment",
        "tlsVersion": "1.3", "cipherSuite": "TLS_CHACHA20_POLY1305_SHA256",
        "keyExchange": "X25519", "signatureAlgorithm": "ECDSA-SHA384", "keySize": 384,
        "certificate": {"issuer": "DigiCert", "expiry": "2027-01-15T23:59:59Z", "serial": "6G:7H:8I:9J"},
        "quantumScore": 50, "status": "warning", "isPublic": True,
        "latitude": 12.9716, "longitude": 77.5946,
        "lastScanAt": "2026-03-10T15:00:00Z", "discoveredAt": "2026-01-25T09:00:00Z",
    },
    {
        "id": "8", "assetId": "imps.pnb.co.in", "domain": "imps.pnb.co.in",
        "ip": "203.123.45.74", "port": 443, "assetType": "payment",
        "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384",
        "keyExchange": "X25519+Kyber768", "signatureAlgorithm": "ECDSA-SHA384", "keySize": 384,
        "certificate": {"issuer": "DigiCert", "expiry": "2027-03-31T23:59:59Z", "serial": "7H:8I:9J:0K"},
        "quantumScore": 72, "status": "scanned", "isPublic": True,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T15:05:00Z", "discoveredAt": "2026-02-10T11:00:00Z",
    },
    {
        "id": "9", "assetId": "swift.pnb.co.in", "domain": "swift.pnb.co.in",
        "ip": "203.123.45.75", "port": 443, "assetType": "banking_core",
        "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384",
        "keyExchange": "ML-KEM-768", "signatureAlgorithm": "ML-DSA-65", "keySize": 768,
        "certificate": {"issuer": "PNB Internal CA", "expiry": "2028-01-01T23:59:59Z", "serial": "8I:9J:0K:1L"},
        "quantumScore": 95, "status": "quantum_safe", "isPublic": False,
        "latitude": 28.6139, "longitude": 77.2090,
        "lastScanAt": "2026-03-10T15:10:00Z", "discoveredAt": "2026-01-10T07:00:00Z",
    },
    {
        "id": "10", "assetId": "cdn.pnb.co.in", "domain": "cdn.pnb.co.in",
        "ip": "203.123.45.76", "port": 443, "assetType": "cdn",
        "tlsVersion": "1.3", "cipherSuite": "TLS_AES_128_GCM_SHA256",
        "keyExchange": "X25519", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048,
        "certificate": {"issuer": "Cloudflare", "expiry": "2026-08-31T23:59:59Z", "serial": "9J:0K:1L:2M"},
        "quantumScore": 35, "status": "warning", "isPublic": True,
        "latitude": 22.5726, "longitude": 88.3639,
        "lastScanAt": "2026-03-10T15:15:00Z", "discoveredAt": "2026-02-05T10:00:00Z",
    },
]


@router.get("")
async def list_assets(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=500),
    status: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "quantumScore",
    sort_order: Optional[str] = "asc",
):
    """List all cryptographic assets with filtering and pagination."""
    filtered = ASSETS.copy()

    if status:
        filtered = [a for a in filtered if a["status"] == status]
    if search:
        search_lower = search.lower()
        filtered = [
            a for a in filtered
            if search_lower in a["domain"].lower()
            or search_lower in a.get("ip", "").lower()
            or search_lower in a.get("cipherSuite", "").lower()
        ]

    # Sort
    reverse = sort_order == "desc"
    if sort_by in ("quantumScore", "keySize", "port"):
        filtered.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    elif sort_by:
        filtered.sort(key=lambda x: str(x.get(sort_by, "")), reverse=reverse)

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]

    return {
        "data": paginated,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/stats")
async def get_asset_stats():
    """Get asset statistics for dashboard."""
    total = len(ASSETS)
    critical = len([a for a in ASSETS if a["status"] == "critical"])
    warning = len([a for a in ASSETS if a["status"] == "warning"])
    secure = len([a for a in ASSETS if a["status"] in ("secure", "quantum_safe")])
    avg_score = sum(a["quantumScore"] for a in ASSETS) / total if total else 0

    return {
        "totalAssets": total,
        "criticalAssets": critical,
        "warningAssets": warning,
        "secureAssets": secure,
        "averageQuantumScore": round(avg_score, 1),
        "pqcReadyPercentage": round(secure / total * 100, 1) if total else 0,
        "scoreDistribution": {
            "critical": len([a for a in ASSETS if a["quantumScore"] < 30]),
            "high": len([a for a in ASSETS if 30 <= a["quantumScore"] < 60]),
            "moderate": len([a for a in ASSETS if 60 <= a["quantumScore"] < 90]),
            "safe": len([a for a in ASSETS if a["quantumScore"] >= 90]),
        },
    }


@router.get("/{asset_id}")
async def get_asset(asset_id: str):
    """Get detailed information for a specific asset."""
    asset = next((a for a in ASSETS if a["assetId"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.get("/{asset_id}/history")
async def get_asset_scan_history(asset_id: str):
    """Get scan history for an asset."""
    return {
        "assetId": asset_id,
        "history": [
            {"date": "2026-03-10", "quantumScore": 15, "status": "critical"},
            {"date": "2026-02-25", "quantumScore": 12, "status": "critical"},
            {"date": "2026-02-10", "quantumScore": 10, "status": "critical"},
            {"date": "2026-01-25", "quantumScore": 8, "status": "critical"},
        ],
    }
