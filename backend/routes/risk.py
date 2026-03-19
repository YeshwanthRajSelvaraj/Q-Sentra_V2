"""
Q-Sentra Risk Route
GET /risk/{asset} - AI-powered risk analysis with blast radius.
"""
from fastapi import APIRouter, Depends
from core.security import get_current_user
from engines.scanner import CryptoScanner
from engines.pqc_validator import PQCValidator
from engines.risk_analyzer import RiskAnalyzer

router = APIRouter(tags=["Risk Analysis"])

# Shared analyzer instance
_analyzer = RiskAnalyzer()
_scan_cache = {}
_graph_built = False


async def _ensure_graph():
    """Build the dependency graph with sample PNB domain assets."""
    global _graph_built
    if _graph_built:
        return

    domain = "pnb.co.in"
    subdomains = [
        "www", "netbanking", "api", "mobile", "vpn", "mail",
        "upi", "swift", "imps", "neft", "cdn", "treasury",
        "portal", "admin", "crm", "hrms", "cards", "loan",
        "sso", "siem",
    ]

    scanner = CryptoScanner()
    validator = PQCValidator()
    assets = []
    scores = {}

    for sub in subdomains:
        host = f"{sub}.{domain}"
        try:
            scan = await scanner.scan(host)
        except Exception:
            scan = scanner._generate_mock_scan(host, 443)
        _scan_cache[host] = scan
        pqc = validator.validate(scan)
        assets.append({
            "domain": host,
            "ip": scan.get("certificate", {}).get("fingerprint_sha256", "")[:8] or "10.0.0.1",
            "port": 443,
        })
        scores[host] = {
            "quantum_score": pqc.get("quantum_score", 50),
            "vulnerabilities": scan.get("vulnerabilities", []),
        }

    _analyzer.build_graph(assets, scores)
    _graph_built = True


@router.get("/risk/{asset}")
async def get_risk(asset: str, user: dict = Depends(get_current_user)):
    """
    Perform AI-powered risk analysis for an asset.
    Returns blast radius, risk scores, attack paths, and community clusters.
    """
    await _ensure_graph()
    result = _analyzer.analyze_risk(target_asset=asset)
    return result


@router.get("/risk/{asset}/blast-radius")
async def get_blast_radius(asset: str, user: dict = Depends(get_current_user)):
    """Get blast radius specifically for a single asset."""
    await _ensure_graph()
    return _analyzer._compute_blast_radius(asset)


@router.get("/risk/graph/topology")
async def get_graph_topology(user: dict = Depends(get_current_user)):
    """Get the full dependency graph as JSON for D3.js/Cytoscape rendering."""
    await _ensure_graph()
    return _analyzer.get_graph_json()
