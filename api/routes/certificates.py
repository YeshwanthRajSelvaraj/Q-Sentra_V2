"""Certificate Management & Blockchain Anchoring routes."""

import hashlib
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()

CERTIFICATES = [
    {"certId": "QCERT-001", "assetId": "swift.pnb.co.in", "quantumScore": 95, "algorithms": ["ML-KEM-768", "ML-DSA-65"], "issuedAt": "2026-03-01T00:00:00Z", "validUntil": "2027-03-01T00:00:00Z", "status": "active", "certificateHash": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678", "blockchainTx": "TX-HLF-98765-ABCDE", "blockNumber": 98765, "issuer": "Q-Sentra PNB Authority", "network": "Hyperledger Fabric"},
    {"certId": "QCERT-002", "assetId": "imps.pnb.co.in", "quantumScore": 72, "algorithms": ["X25519+Kyber768", "ECDSA-SHA384"], "issuedAt": "2026-02-15T00:00:00Z", "validUntil": "2027-02-15T00:00:00Z", "status": "active", "certificateHash": "b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456789a", "blockchainTx": "TX-HLF-98764-BCDEF", "blockNumber": 98764, "issuer": "Q-Sentra PNB Authority", "network": "Hyperledger Fabric"},
]


@router.get("")
async def list_certificates():
    return {"data": CERTIFICATES, "total": len(CERTIFICATES)}


@router.get("/{cert_id}")
async def get_certificate(cert_id: str):
    cert = next((c for c in CERTIFICATES if c["certId"] == cert_id), None)
    if not cert: raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@router.post("/issue")
async def issue_certificate(asset_id: str, quantum_score: int = 90):
    if quantum_score < 90:
        raise HTTPException(status_code=400, detail="Quantum score must be >= 90 for certificate issuance")
    cert_data = {"assetId": asset_id, "score": quantum_score, "algorithms": ["ML-KEM-768", "ML-DSA-65"], "issuedAt": datetime.utcnow().isoformat() + "Z"}
    cert_hash = hashlib.sha3_256(str(cert_data).encode()).hexdigest()
    return {"certId": f"QCERT-{datetime.utcnow().strftime('%Y%m%d%H%M')}", "assetId": asset_id, "certificateHash": cert_hash, "blockchainTx": f"TX-HLF-{98766}-DEMO", "status": "pending_anchor"}


@router.get("/{cert_id}/verify")
async def verify_certificate(cert_id: str):
    cert = next((c for c in CERTIFICATES if c["certId"] == cert_id), None)
    if not cert: raise HTTPException(status_code=404, detail="Certificate not found")
    return {"verified": True, "certificate": cert, "blockchainProof": {"txId": cert["blockchainTx"], "blockNumber": cert["blockNumber"], "network": cert["network"], "explorerUrl": f"https://explorer.hlf.pnb.co.in/tx/{cert['blockchainTx']}", "timestamp": cert["issuedAt"]}}
