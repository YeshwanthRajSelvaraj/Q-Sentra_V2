"""PQC Validation Engine routes."""

from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()


def calculate_quantum_score(tls_version, key_exchange, signature, key_size):
    tls_scores = {"1.3": 20, "1.2": 5, "1.1": 0, "1.0": 0}
    tls_score = tls_scores.get(tls_version, 0)
    kex_scores = {"ML-KEM-768": 35, "ML-KEM-1024": 35, "ML-KEM-512": 30, "X25519+Kyber768": 20, "X25519": 10, "ECDHE": 10, "RSA": 0}
    kex_score = kex_scores.get(key_exchange, 0)
    sig_scores = {"ML-DSA-87": 30, "ML-DSA-65": 30, "ML-DSA-44": 28, "SLH-DSA-256f": 30, "ECDSA-SHA384": 10, "ECDSA-SHA256": 10, "RSA-SHA256": 0}
    sig_score = sig_scores.get(signature, 0)
    keysize_score = 15 if "ML-KEM" in key_exchange else (5 if key_size >= 4096 else 0)
    total = min(100, tls_score + kex_score + sig_score + keysize_score)
    if total >= 90: category, risk = "Fully Quantum Safe", "low"
    elif total >= 60: category, risk = "PQC Transitioning", "moderate"
    elif total >= 30: category, risk = "HNDL Risk", "high"
    else: category, risk = "Critical Exposure", "severe"
    return {"quantumScore": total, "breakdown": {"tls": {"score": tls_score, "max": 20, "value": tls_version}, "keyExchange": {"score": kex_score, "max": 35, "value": key_exchange}, "signature": {"score": sig_score, "max": 30, "value": signature}, "keySize": {"score": keysize_score, "max": 15, "value": key_size}}, "riskCategory": category, "riskLevel": risk, "compliance": {"fips203": "ML-KEM" in key_exchange, "fips204": "ML-DSA" in signature, "fips205": "SLH-DSA" in signature}}


ASSETS = [
    {"assetId": "web01.pnb.co.in", "tlsVersion": "1.2", "keyExchange": "RSA", "sig": "RSA-SHA256", "keySize": 2048},
    {"assetId": "netbanking.pnb.co.in", "tlsVersion": "1.2", "keyExchange": "ECDHE", "sig": "RSA-SHA256", "keySize": 2048},
    {"assetId": "api.pnb.co.in", "tlsVersion": "1.3", "keyExchange": "X25519", "sig": "ECDSA-SHA384", "keySize": 384},
    {"assetId": "mobile.pnb.co.in", "tlsVersion": "1.3", "keyExchange": "X25519", "sig": "ECDSA-SHA256", "keySize": 256},
    {"assetId": "vpn.pnb.co.in", "tlsVersion": "1.2", "keyExchange": "RSA", "sig": "RSA-SHA256", "keySize": 4096},
    {"assetId": "mail.pnb.co.in", "tlsVersion": "1.2", "keyExchange": "ECDHE", "sig": "RSA-SHA256", "keySize": 2048},
    {"assetId": "upi.pnb.co.in", "tlsVersion": "1.3", "keyExchange": "X25519", "sig": "ECDSA-SHA384", "keySize": 384},
    {"assetId": "imps.pnb.co.in", "tlsVersion": "1.3", "keyExchange": "X25519+Kyber768", "sig": "ECDSA-SHA384", "keySize": 384},
    {"assetId": "swift.pnb.co.in", "tlsVersion": "1.3", "keyExchange": "ML-KEM-768", "sig": "ML-DSA-65", "keySize": 768},
    {"assetId": "cdn.pnb.co.in", "tlsVersion": "1.3", "keyExchange": "X25519", "sig": "RSA-SHA256", "keySize": 2048},
]


@router.get("/validate/{asset_id}")
async def validate_asset(asset_id: str):
    asset = next((a for a in ASSETS if a["assetId"] == asset_id), None)
    if not asset: raise HTTPException(status_code=404, detail="Asset not found")
    result = calculate_quantum_score(asset["tlsVersion"], asset["keyExchange"], asset["sig"], asset["keySize"])
    result["assetId"] = asset_id
    result["validatedAt"] = datetime.utcnow().isoformat() + "Z"
    return result


@router.get("/validate-all")
async def validate_all():
    results = []
    for a in ASSETS:
        r = calculate_quantum_score(a["tlsVersion"], a["keyExchange"], a["sig"], a["keySize"])
        r["assetId"] = a["assetId"]
        results.append(r)
    return {"totalAssets": len(results), "validated": results, "summary": {"fullyQuantumSafe": len([r for r in results if r["quantumScore"] >= 90]), "transitioning": len([r for r in results if 60 <= r["quantumScore"] < 90]), "hndlRisk": len([r for r in results if 30 <= r["quantumScore"] < 60]), "criticalExposure": len([r for r in results if r["quantumScore"] < 30])}}


@router.get("/standards")
async def get_standards():
    return {"standards": [
        {"fips": "203", "name": "ML-KEM (Kyber)", "type": "KEM", "keySizes": [512, 768, 1024]},
        {"fips": "204", "name": "ML-DSA (Dilithium)", "type": "Signature", "parameterSets": [44, 65, 87]},
        {"fips": "205", "name": "SLH-DSA (SPHINCS+)", "type": "Signature", "parameterSets": ["128f", "128s", "192f", "192s", "256f", "256s"]},
    ]}
