"""
Q-Sentra Remediation Route
GET /remediate/{asset} - Generate remediation playbook.
"""
from fastapi import APIRouter, Depends, Response
from core.security import get_current_user
from engines.scanner import CryptoScanner
from engines.pqc_validator import PQCValidator
from engines.remediation import RemediationOrchestrator

router = APIRouter(tags=["Remediation"])
_scan_cache = {}


@router.get("/remediate/{asset}")
async def remediate_asset(asset: str, format: str = "json",
                          user: dict = Depends(get_current_user)):
    """
    Generate remediation playbook for an asset.

    Query params:
      - format: json (default), markdown, yaml, nginx, apache
    """
    # Scan + PQC validation
    if asset not in _scan_cache:
        scanner = CryptoScanner()
        _scan_cache[asset] = await scanner.scan(asset)

    scan = _scan_cache[asset]
    pqc = PQCValidator().validate(scan)
    remediation = RemediationOrchestrator().generate(asset, scan, pqc)

    if format == "markdown":
        return Response(
            content=remediation["playbook_markdown"],
            media_type="text/markdown",
        )
    elif format == "yaml":
        return Response(
            content=remediation["playbook_ansible"],
            media_type="text/yaml",
        )
    elif format == "nginx":
        return Response(
            content=remediation["configs"]["nginx"],
            media_type="text/plain",
        )
    elif format == "apache":
        return Response(
            content=remediation["configs"]["apache"],
            media_type="text/plain",
        )

    return remediation
