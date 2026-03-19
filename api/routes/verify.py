"""Public Certificate Verification Portal - No Auth Required."""

from fastapi import APIRouter, HTTPException

router = APIRouter()

CERTS = {
    "swift.pnb.co.in": {"certId": "QCERT-001", "assetId": "swift.pnb.co.in", "quantumScore": 95, "algorithms": ["ML-KEM-768", "ML-DSA-65"], "issuedAt": "2026-03-01T00:00:00Z", "validUntil": "2027-03-01T00:00:00Z", "status": "active", "certificateHash": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678", "blockchainTx": "TX-HLF-98765-ABCDE", "blockNumber": 98765, "network": "Hyperledger Fabric", "issuer": "Q-Sentra PNB Authority"},
    "imps.pnb.co.in": {"certId": "QCERT-002", "assetId": "imps.pnb.co.in", "quantumScore": 72, "algorithms": ["X25519+Kyber768", "ECDSA-SHA384"], "issuedAt": "2026-02-15T00:00:00Z", "validUntil": "2027-02-15T00:00:00Z", "status": "active", "certificateHash": "b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456789a", "blockchainTx": "TX-HLF-98764-BCDEF", "blockNumber": 98764, "network": "Hyperledger Fabric", "issuer": "Q-Sentra PNB Authority"},
}


@router.get("/{asset_id}")
async def verify_asset_certificate(asset_id: str):
    cert = CERTS.get(asset_id)
    if not cert: raise HTTPException(status_code=404, detail="No quantum-safe certificate found for this asset")
    return {"verified": True, "certificate": cert, "blockchainProof": {"txId": cert["blockchainTx"], "blockNumber": cert["blockNumber"], "network": cert["network"], "explorerUrl": f"https://explorer.hlf.pnb.co.in/tx/{cert['blockchainTx']}"}}
