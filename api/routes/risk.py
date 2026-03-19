"""Risk Analysis routes - HNDL forecasting and blast radius."""

from fastapi import APIRouter, HTTPException

router = APIRouter()

HNDL_DATA = [
    {"assetId": "web01.pnb.co.in", "dataValue": 7, "exposure": 0.9, "quantumScore": 15, "yearsTocrqc": 7.0, "hndlRisk": 96.4, "liabilityINR": 5000000000, "attackVector": "Public web portal → RSA key harvest → Future decryption of session data", "priority": 1},
    {"assetId": "netbanking.pnb.co.in", "dataValue": 10, "exposure": 0.95, "quantumScore": 25, "yearsTocrqc": 7.0, "hndlRisk": 101.8, "liabilityINR": 25000000000, "attackVector": "Net banking session → RSA-2048 KEX harvest → Account data decryption", "priority": 1},
    {"assetId": "api.pnb.co.in", "dataValue": 8, "exposure": 0.8, "quantumScore": 45, "yearsTocrqc": 7.0, "hndlRisk": 62.9, "liabilityINR": 8000000000, "attackVector": "API gateway → X25519 KEX → Post-quantum key recovery", "priority": 2},
    {"assetId": "mobile.pnb.co.in", "dataValue": 7, "exposure": 0.7, "quantumScore": 40, "yearsTocrqc": 7.0, "hndlRisk": 42.0, "liabilityINR": 4000000000, "attackVector": "Mobile API → ECDSA harvest → Transaction replay", "priority": 2},
    {"assetId": "vpn.pnb.co.in", "dataValue": 9, "exposure": 0.3, "quantumScore": 20, "yearsTocrqc": 7.0, "hndlRisk": 30.9, "liabilityINR": 4000000000, "attackVector": "VPN tunnel harvest → Internal network decryption", "priority": 2},
    {"assetId": "mail.pnb.co.in", "dataValue": 6, "exposure": 0.6, "quantumScore": 30, "yearsTocrqc": 7.0, "hndlRisk": 36.0, "liabilityINR": 2000000000, "attackVector": "Email interception → RSA harvest → Confidential comms exposure", "priority": 3},
    {"assetId": "upi.pnb.co.in", "dataValue": 10, "exposure": 0.9, "quantumScore": 50, "yearsTocrqc": 7.0, "hndlRisk": 64.3, "liabilityINR": 30000000000, "attackVector": "UPI transactions → ECDHE harvest → Payment data exposure", "priority": 1},
    {"assetId": "imps.pnb.co.in", "dataValue": 9, "exposure": 0.7, "quantumScore": 72, "yearsTocrqc": 7.0, "hndlRisk": 25.2, "liabilityINR": 5000000000, "attackVector": "Partially mitigated - Hybrid KEM active", "priority": 3},
    {"assetId": "swift.pnb.co.in", "dataValue": 10, "exposure": 0.1, "quantumScore": 95, "yearsTocrqc": 7.0, "hndlRisk": 0.7, "liabilityINR": 500000000, "attackVector": "Low risk - ML-KEM-768 quantum-safe", "priority": 4},
    {"assetId": "cdn.pnb.co.in", "dataValue": 4, "exposure": 0.8, "quantumScore": 35, "yearsTocrqc": 7.0, "hndlRisk": 29.7, "liabilityINR": 1000000000, "attackVector": "CDN edge → RSA sig harvest → Content integrity risk", "priority": 3},
]

BLAST_RADIUS = {
    "nodes": [
        {"id": "web01.pnb.co.in", "quantumScore": 15, "blastRadius": 0.45, "type": "web", "label": "Web Portal"},
        {"id": "netbanking.pnb.co.in", "quantumScore": 25, "blastRadius": 0.72, "type": "web", "label": "Net Banking"},
        {"id": "api.pnb.co.in", "quantumScore": 45, "blastRadius": 0.85, "type": "api", "label": "API Gateway"},
        {"id": "mobile.pnb.co.in", "quantumScore": 40, "blastRadius": 0.38, "type": "mobile", "label": "Mobile API"},
        {"id": "vpn.pnb.co.in", "quantumScore": 20, "blastRadius": 0.55, "type": "vpn", "label": "VPN Gateway"},
        {"id": "mail.pnb.co.in", "quantumScore": 30, "blastRadius": 0.25, "type": "email", "label": "Mail Server"},
        {"id": "upi.pnb.co.in", "quantumScore": 50, "blastRadius": 0.65, "type": "payment", "label": "UPI Gateway"},
        {"id": "imps.pnb.co.in", "quantumScore": 72, "blastRadius": 0.48, "type": "payment", "label": "IMPS"},
        {"id": "swift.pnb.co.in", "quantumScore": 95, "blastRadius": 0.92, "type": "core", "label": "SWIFT"},
        {"id": "cdn.pnb.co.in", "quantumScore": 35, "blastRadius": 0.2, "type": "cdn", "label": "CDN"},
    ],
    "edges": [
        {"source": "web01.pnb.co.in", "target": "api.pnb.co.in", "weight": 0.9},
        {"source": "netbanking.pnb.co.in", "target": "api.pnb.co.in", "weight": 0.95},
        {"source": "mobile.pnb.co.in", "target": "api.pnb.co.in", "weight": 0.9},
        {"source": "api.pnb.co.in", "target": "swift.pnb.co.in", "weight": 1.0},
        {"source": "api.pnb.co.in", "target": "upi.pnb.co.in", "weight": 0.85},
        {"source": "api.pnb.co.in", "target": "imps.pnb.co.in", "weight": 0.85},
        {"source": "upi.pnb.co.in", "target": "swift.pnb.co.in", "weight": 0.95},
        {"source": "imps.pnb.co.in", "target": "swift.pnb.co.in", "weight": 0.95},
        {"source": "mail.pnb.co.in", "target": "vpn.pnb.co.in", "weight": 0.5},
        {"source": "web01.pnb.co.in", "target": "cdn.pnb.co.in", "weight": 0.7},
    ],
}


@router.get("/hndl")
async def get_hndl_risks():
    total_liability = sum(h["liabilityINR"] for h in HNDL_DATA)
    return {"totalLiabilityINR": total_liability, "totalLiabilityCrore": round(total_liability / 10000000, 0), "assessments": HNDL_DATA, "yearsToQDay": 7.0}


@router.get("/hndl/{asset_id}")
async def get_asset_hndl(asset_id: str):
    h = next((x for x in HNDL_DATA if x["assetId"] == asset_id), None)
    if not h: raise HTTPException(status_code=404, detail="Not found")
    return h


@router.get("/blast-radius")
async def get_blast_radius():
    return BLAST_RADIUS


@router.get("/threat-intel")
async def get_threat_intel():
    return {"threats": [
        {"id": "TI-001", "source": "CISA", "title": "Quantum Computing Threat Advisory", "severity": "critical", "date": "2026-02-15", "mitre": "T1557"},
        {"id": "TI-002", "source": "MITRE ATT&CK", "title": "HNDL Campaign Indicators", "severity": "high", "date": "2026-03-01", "mitre": "T1040"},
        {"id": "TI-003", "source": "NIST", "title": "PQC Migration Urgency Update", "severity": "high", "date": "2026-03-05", "mitre": "N/A"},
    ]}
