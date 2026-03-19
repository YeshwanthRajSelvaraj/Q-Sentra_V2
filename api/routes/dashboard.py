"""Dashboard analytics routes."""

from datetime import datetime, timedelta
from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview():
    return {
        "kpis": {
            "totalAssets": 10,
            "pqcReadyPercentage": 10.0,
            "averageQuantumScore": 42.7,
            "hndlRisksCount": 7,
            "criticalAssets": 3,
            "totalLiabilityCrore": 8450,
            "activeCertificates": 2,
            "remediationProgress": 11.1,
        },
        "scoreDistribution": [
            {"range": "0-29", "label": "Critical", "count": 4, "color": "#EF4444"},
            {"range": "30-59", "label": "High Risk", "count": 4, "color": "#F97316"},
            {"range": "60-89", "label": "Moderate", "count": 1, "color": "#EAB308"},
            {"range": "90-100", "label": "Safe", "count": 1, "color": "#22C55E"},
        ],
        "recentActivity": [
            {"id": 1, "type": "scan", "message": "Full scan completed on swift.pnb.co.in", "severity": "info", "timestamp": "2026-03-10T15:10:00Z"},
            {"id": 2, "type": "alert", "message": "Critical: web01.pnb.co.in using RSA key exchange", "severity": "critical", "timestamp": "2026-03-10T14:30:00Z"},
            {"id": 3, "type": "remediation", "message": "REM-002 started: Net banking PQC migration", "severity": "info", "timestamp": "2026-03-10T12:00:00Z"},
            {"id": 4, "type": "certificate", "message": "QCERT-001 issued for swift.pnb.co.in", "severity": "success", "timestamp": "2026-03-01T00:00:00Z"},
            {"id": 5, "type": "discovery", "message": "New asset discovered: cdn.pnb.co.in", "severity": "info", "timestamp": "2026-02-05T10:00:00Z"},
            {"id": 6, "type": "alert", "message": "HNDL Risk: netbanking.pnb.co.in liability ₹2,500 Cr", "severity": "critical", "timestamp": "2026-03-10T14:35:00Z"},
        ],
        "assetMap": [
            {"id": "web01.pnb.co.in", "lat": 28.6139, "lng": 77.2090, "score": 15, "label": "Web Portal", "city": "New Delhi"},
            {"id": "netbanking.pnb.co.in", "lat": 28.6339, "lng": 77.2200, "score": 25, "label": "Net Banking", "city": "New Delhi"},
            {"id": "api.pnb.co.in", "lat": 28.5939, "lng": 77.1890, "score": 45, "label": "API Gateway", "city": "New Delhi"},
            {"id": "mobile.pnb.co.in", "lat": 19.0760, "lng": 72.8777, "score": 40, "label": "Mobile API", "city": "Mumbai"},
            {"id": "vpn.pnb.co.in", "lat": 28.6439, "lng": 77.2390, "score": 20, "label": "VPN Gateway", "city": "New Delhi"},
            {"id": "mail.pnb.co.in", "lat": 28.5839, "lng": 77.1990, "score": 30, "label": "Mail Server", "city": "New Delhi"},
            {"id": "upi.pnb.co.in", "lat": 12.9716, "lng": 77.5946, "score": 50, "label": "UPI Gateway", "city": "Bangalore"},
            {"id": "imps.pnb.co.in", "lat": 28.6039, "lng": 77.2290, "score": 72, "label": "IMPS", "city": "New Delhi"},
            {"id": "swift.pnb.co.in", "lat": 28.6239, "lng": 77.2190, "score": 95, "label": "SWIFT Core", "city": "New Delhi"},
            {"id": "cdn.pnb.co.in", "lat": 22.5726, "lng": 88.3639, "score": 35, "label": "CDN Edge", "city": "Kolkata"},
        ],
        "trendData": [
            {"date": "2026-01", "avgScore": 18, "assets": 5},
            {"date": "2026-02", "avgScore": 28, "assets": 8},
            {"date": "2026-03", "avgScore": 42.7, "assets": 10},
        ],
    }


@router.get("/compliance")
async def get_compliance_status():
    return {"frameworks": [
        {"name": "NIST PQC (FIPS 203/204/205)", "status": "partial", "coverage": 10, "details": "1/10 assets fully compliant"},
        {"name": "RBI Digital Payment Security", "status": "compliant", "coverage": 85, "details": "Encryption controls in place"},
        {"name": "PCI-DSS v4.0 Req 4", "status": "partial", "coverage": 60, "details": "TLS 1.3 migration in progress"},
        {"name": "ISO 27001:2022 A.8.24", "status": "compliant", "coverage": 90, "details": "Cryptographic lifecycle management active"},
        {"name": "GDPR Article 32", "status": "compliant", "coverage": 80, "details": "State-of-art encryption measures"},
        {"name": "India DPDP Act 2023", "status": "compliant", "coverage": 75, "details": "Personal data protection controls active"},
    ]}
