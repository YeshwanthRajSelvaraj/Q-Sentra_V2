"""CBOM (Cryptographic Bill of Materials) routes."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

router = APIRouter()


def generate_cbom(asset: dict) -> dict:
    """Generate CycloneDX 1.6 compliant CBOM for an asset."""
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:qsentra-cbom-{asset['assetId'].replace('.', '-')}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tools": [{
                "vendor": "Q-Sentra",
                "name": "PNB Quantum CBOM Generator",
                "version": "1.0.0",
            }],
            "authors": [{"name": "PNB Cybersecurity Team", "email": "cybersecurity@pnb.co.in"}],
            "component": {
                "type": "application",
                "name": asset["assetId"],
                "version": "1.0",
            },
        },
        "components": [
            {
                "type": "crypto-asset",
                "name": f"tls-config-{asset['assetId']}",
                "version": asset.get("tlsVersion", "unknown"),
                "cryptoProperties": {
                    "assetType": "protocol",
                    "algorithmProperties": {
                        "variant": asset.get("cipherSuite", "unknown"),
                        "primitive": "block-cipher",
                        "parameterSetIdentifier": asset.get("cipherSuite", ""),
                    },
                    "protocolProperties": {
                        "type": "TLS",
                        "version": asset.get("tlsVersion", "unknown"),
                        "cipherSuites": [{"name": asset.get("cipherSuite", "unknown")}],
                    },
                },
                "properties": [
                    {"name": "quantumSafetyScore", "value": str(asset.get("quantumScore", 0))},
                    {"name": "keyExchange", "value": asset.get("keyExchange", "unknown")},
                    {"name": "signatureAlgorithm", "value": asset.get("signatureAlgorithm", "unknown")},
                    {"name": "keySize", "value": str(asset.get("keySize", 0))},
                    {"name": "nistCompliance", "value": "FIPS 203/204/205" if asset.get("quantumScore", 0) >= 90 else "Non-compliant"},
                ],
            },
            {
                "type": "crypto-asset",
                "name": f"kex-{asset.get('keyExchange', 'unknown')}",
                "cryptoProperties": {
                    "assetType": "algorithm",
                    "algorithmProperties": {
                        "variant": asset.get("keyExchange", "unknown"),
                        "primitive": "key-agree" if "DH" in asset.get("keyExchange", "") or "KEM" in asset.get("keyExchange", "") else "key-encapsulation",
                        "implementationPlatform": "software",
                        "certificationLevel": "FIPS 203" if "ML-KEM" in asset.get("keyExchange", "") else "none",
                    },
                },
            },
            {
                "type": "crypto-asset",
                "name": f"sig-{asset.get('signatureAlgorithm', 'unknown')}",
                "cryptoProperties": {
                    "assetType": "algorithm",
                    "algorithmProperties": {
                        "variant": asset.get("signatureAlgorithm", "unknown"),
                        "primitive": "signature",
                        "certificationLevel": "FIPS 204" if "ML-DSA" in asset.get("signatureAlgorithm", "") else "none",
                    },
                },
            },
        ],
        "vulnerabilities": _get_crypto_vulnerabilities(asset),
    }


def _get_crypto_vulnerabilities(asset: dict) -> list:
    """Identify cryptographic vulnerabilities."""
    vulns = []
    kex = asset.get("keyExchange", "")
    sig = asset.get("signatureAlgorithm", "")
    tls = asset.get("tlsVersion", "")

    if "RSA" in kex:
        vulns.append({
            "id": "QVULN-001",
            "description": "RSA key exchange vulnerable to Shor's algorithm on quantum computers",
            "severity": "critical",
            "recommendation": "Migrate to ML-KEM-768 (FIPS 203)",
        })
    if kex in ("ECDHE", "X25519") and "Kyber" not in kex and "ML-KEM" not in kex:
        vulns.append({
            "id": "QVULN-002",
            "description": "Elliptic curve key exchange vulnerable to quantum attacks",
            "severity": "high",
            "recommendation": "Implement hybrid X25519+Kyber768 or migrate to ML-KEM-768",
        })
    if "RSA" in sig:
        vulns.append({
            "id": "QVULN-003",
            "description": "RSA signature algorithm vulnerable to quantum forgery",
            "severity": "high",
            "recommendation": "Migrate to ML-DSA-65 (FIPS 204) or SLH-DSA (FIPS 205)",
        })
    if tls < "1.3":
        vulns.append({
            "id": "QVULN-004",
            "description": f"TLS {tls} lacks native PQC negotiation support",
            "severity": "medium",
            "recommendation": "Upgrade to TLS 1.3 for PQC cipher suite support",
        })
    return vulns


# Sample CBOM data for all assets
ASSET_DATA = [
    {"assetId": "web01.pnb.co.in", "tlsVersion": "1.2", "cipherSuite": "TLS_RSA_WITH_AES_128_CBC_SHA", "keyExchange": "RSA", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048, "quantumScore": 15},
    {"assetId": "netbanking.pnb.co.in", "tlsVersion": "1.2", "cipherSuite": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "keyExchange": "ECDHE", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048, "quantumScore": 25},
    {"assetId": "api.pnb.co.in", "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384", "keyExchange": "X25519", "signatureAlgorithm": "ECDSA-SHA384", "keySize": 384, "quantumScore": 45},
    {"assetId": "mobile.pnb.co.in", "tlsVersion": "1.3", "cipherSuite": "TLS_AES_128_GCM_SHA256", "keyExchange": "X25519", "signatureAlgorithm": "ECDSA-SHA256", "keySize": 256, "quantumScore": 40},
    {"assetId": "vpn.pnb.co.in", "tlsVersion": "1.2", "cipherSuite": "TLS_RSA_WITH_AES_256_CBC_SHA256", "keyExchange": "RSA", "signatureAlgorithm": "RSA-SHA256", "keySize": 4096, "quantumScore": 20},
    {"assetId": "mail.pnb.co.in", "tlsVersion": "1.2", "cipherSuite": "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256", "keyExchange": "ECDHE", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048, "quantumScore": 30},
    {"assetId": "upi.pnb.co.in", "tlsVersion": "1.3", "cipherSuite": "TLS_CHACHA20_POLY1305_SHA256", "keyExchange": "X25519", "signatureAlgorithm": "ECDSA-SHA384", "keySize": 384, "quantumScore": 50},
    {"assetId": "imps.pnb.co.in", "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384", "keyExchange": "X25519+Kyber768", "signatureAlgorithm": "ECDSA-SHA384", "keySize": 384, "quantumScore": 72},
    {"assetId": "swift.pnb.co.in", "tlsVersion": "1.3", "cipherSuite": "TLS_AES_256_GCM_SHA384", "keyExchange": "ML-KEM-768", "signatureAlgorithm": "ML-DSA-65", "keySize": 768, "quantumScore": 95},
    {"assetId": "cdn.pnb.co.in", "tlsVersion": "1.3", "cipherSuite": "TLS_AES_128_GCM_SHA256", "keyExchange": "X25519", "signatureAlgorithm": "RSA-SHA256", "keySize": 2048, "quantumScore": 35},
]


@router.get("")
async def list_cboms(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50)):
    """List all generated CBOMs."""
    cboms = [generate_cbom(a) for a in ASSET_DATA]
    start = (page - 1) * limit
    return {
        "data": cboms[start:start + limit],
        "pagination": {"page": page, "limit": limit, "total": len(cboms)},
    }


@router.get("/{asset_id}")
async def get_cbom(asset_id: str, format: Optional[str] = Query("json", regex="^(json|xml|csv)$")):
    """Get CBOM for a specific asset."""
    asset = next((a for a in ASSET_DATA if a["assetId"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return generate_cbom(asset)


@router.get("/{asset_id}/export")
async def export_cbom(asset_id: str, format: str = Query("json", regex="^(json|xml|csv|pdf)$")):
    """Export CBOM in specified format."""
    asset = next((a for a in ASSET_DATA if a["assetId"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    cbom = generate_cbom(asset)
    return JSONResponse(
        content=cbom,
        headers={"Content-Disposition": f"attachment; filename=cbom-{asset_id}.{format}"},
    )
