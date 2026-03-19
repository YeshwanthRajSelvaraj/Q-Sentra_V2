"""
Q-Sentra Certificate Routes
GET /certificate/{asset} - Issue quantum-safe certificate.
GET /verify/{asset} - Public certificate verification (no auth required).
"""
from fastapi import APIRouter, Depends
from core.security import get_current_user
from engines.scanner import CryptoScanner
from engines.pqc_validator import PQCValidator
from engines.certificate_mgr import CertificateManager

router = APIRouter(tags=["Certificates"])

# Shared certificate manager
_cert_mgr = CertificateManager()
_scan_cache = {}


@router.get("/certificate/{asset}")
async def issue_certificate(asset: str, user: dict = Depends(get_current_user)):
    """
    Issue a quantum-safe certificate for an asset (requires score ≥ 90).
    Certificate is hashed with SHA3-256 and anchored to blockchain ledger.
    """
    # Scan + PQC validation
    if asset not in _scan_cache:
        scanner = CryptoScanner()
        _scan_cache[asset] = await scanner.scan(asset)

    scan = _scan_cache[asset]
    pqc = PQCValidator().validate(scan)

    result = _cert_mgr.issue_certificate(asset, asset, scan, pqc)
    return result


@router.get("/verify/{cert_id}")
async def verify_certificate(cert_id: str):
    """
    Public endpoint: Verify a quantum-safe certificate.
    No authentication required — anyone can verify.
    """
    return _cert_mgr.verify_certificate(cert_id)


@router.get("/certificates")
async def list_certificates(user: dict = Depends(get_current_user)):
    """List all issued certificates."""
    return _cert_mgr.list_certificates()


@router.get("/certificates/ledger")
async def get_blockchain_ledger(user: dict = Depends(get_current_user)):
    """Get the full blockchain ledger for auditing."""
    return _cert_mgr.get_ledger()
