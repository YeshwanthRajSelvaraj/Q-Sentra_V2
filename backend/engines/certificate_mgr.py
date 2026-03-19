"""
Q-Sentra Certificate Management Engine
Issues quantum-safe certificates, hashes with SHA3-256,
and maintains a simulated blockchain ledger for verification.

Features:
  - JSON certificate generation for high-scoring assets (≥90)
  - SHA3-256 certificate hashing
  - Simulated blockchain ledger (simple append-only DB)
  - Certificate verification endpoint support
"""
import uuid
import hashlib
import json
import logging
from typing import Dict, Optional, List
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("qsentra.certificate")


class CertificateManager:
    """Issues and verifies quantum-safe certificates with blockchain anchoring."""

    MINIMUM_SCORE = 90  # Minimum quantum score to issue certificate
    VALIDITY_DAYS = 365
    ISSUER = "Q-Sentra Quantum Certificate Authority"

    def __init__(self):
        # In-memory blockchain ledger (simulates distributed ledger)
        self._ledger: List[Dict] = []
        self._certificates: Dict[str, Dict] = {}

    def issue_certificate(self, asset_id: str, host: str,
                         scan_result: Dict, pqc_result: Dict) -> Dict:
        """
        Issue a quantum-safe certificate for an asset.

        Args:
            asset_id: Unique asset identifier
            host: Hostname
            scan_result: Output from CryptoScanner
            pqc_result: Output from PQCValidator

        Returns:
            Certificate document or rejection reason
        """
        score = pqc_result.get("quantum_score", 0)

        if score < self.MINIMUM_SCORE:
            return {
                "status": "rejected",
                "reason": f"Quantum score {score} is below minimum threshold {self.MINIMUM_SCORE}",
                "current_score": score,
                "required_score": self.MINIMUM_SCORE,
                "recommendations": pqc_result.get("recommendations", []),
            }

        # ── Generate Certificate ──
        cert_id = f"QSC-{uuid.uuid4().hex[:12].upper()}"
        now = datetime.now(timezone.utc)
        expiry = now + timedelta(days=self.VALIDITY_DAYS)

        certificate = {
            "certificate_id": cert_id,
            "version": 1,
            "asset_id": asset_id,
            "host": host,
            "subject": {
                "common_name": host,
                "organization": "Punjab National Bank",
                "country": "IN",
                "state": "Delhi",
            },
            "issuer": {
                "common_name": self.ISSUER,
                "organization": "Q-Sentra Platform",
                "country": "IN",
            },
            "validity": {
                "not_before": now.isoformat(),
                "not_after": expiry.isoformat(),
                "valid_days": self.VALIDITY_DAYS,
            },
            "quantum_attestation": {
                "quantum_score": score,
                "risk_category": pqc_result.get("risk_category", "minimal"),
                "tls_version": scan_result.get("tls_version", ""),
                "key_exchange": scan_result.get("key_exchange", ""),
                "cipher_suite": scan_result.get("cipher_suite", ""),
                "pqc_algorithms_detected": self._detect_pqc_algos(scan_result),
                "hndl_risk": pqc_result.get("hndl_risk", {}),
            },
            "compliance": {
                "nist_pqc": True,
                "fips_203": pqc_result.get("breakdown", {}).get("pqc_readiness", {}).get("details", {}).get("has_pqc_kex", False),
                "fips_204": pqc_result.get("breakdown", {}).get("pqc_readiness", {}).get("details", {}).get("has_pqc_sig", False),
            },
            "issued_at": now.isoformat(),
            "status": "active",
        }

        # ── SHA3-256 Hash ──
        cert_json = json.dumps(certificate, sort_keys=True)
        cert_hash = hashlib.sha3_256(cert_json.encode()).hexdigest()
        certificate["sha3_256_hash"] = cert_hash

        # ── Blockchain Anchoring ──
        tx = self._anchor_to_blockchain(cert_id, cert_hash, now)
        certificate["blockchain"] = tx

        # Store
        self._certificates[cert_id] = certificate

        logger.info(f"Issued certificate {cert_id} for {host} (score: {score})")
        return {
            "status": "issued",
            "certificate": certificate,
        }

    def verify_certificate(self, cert_id: str) -> Dict:
        """
        Verify a certificate's authenticity and blockchain anchoring.

        Returns:
            Verification result with integrity check
        """
        cert = self._certificates.get(cert_id)
        if not cert:
            return {
                "status": "not_found",
                "message": f"Certificate {cert_id} not found in registry",
                "verified": False,
            }

        # ── Recompute Hash ──
        stored_hash = cert.get("sha3_256_hash", "")
        cert_copy = {k: v for k, v in cert.items() if k not in ("sha3_256_hash", "blockchain")}
        recomputed_hash = hashlib.sha3_256(
            json.dumps(cert_copy, sort_keys=True).encode()
        ).hexdigest()
        hash_valid = stored_hash == recomputed_hash

        # ── Check Blockchain Ledger ──
        tx_hash = cert.get("blockchain", {}).get("tx_hash", "")
        blockchain_valid = any(tx["tx_hash"] == tx_hash for tx in self._ledger)

        # ── Check Expiry ──
        expiry_str = cert.get("validity", {}).get("not_after", "")
        try:
            expiry = datetime.fromisoformat(expiry_str)
            is_expired = datetime.now(timezone.utc) > expiry
        except Exception:
            is_expired = True

        return {
            "status": "verified" if (hash_valid and blockchain_valid and not is_expired) else "invalid",
            "certificate_id": cert_id,
            "host": cert.get("host", ""),
            "quantum_score": cert.get("quantum_attestation", {}).get("quantum_score", 0),
            "checks": {
                "hash_integrity": {
                    "valid": hash_valid,
                    "algorithm": "SHA3-256",
                    "stored_hash": stored_hash[:16] + "...",
                    "computed_hash": recomputed_hash[:16] + "...",
                },
                "blockchain_anchoring": {
                    "valid": blockchain_valid,
                    "network": "Q-Sentra Ledger (Hyperledger Fabric Simulated)",
                    "tx_hash": tx_hash[:16] + "..." if tx_hash else "none",
                },
                "validity_period": {
                    "valid": not is_expired,
                    "not_after": expiry_str,
                    "is_expired": is_expired,
                },
            },
            "verified": hash_valid and blockchain_valid and not is_expired,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }

    def list_certificates(self) -> List[Dict]:
        """List all issued certificates."""
        return [
            {
                "certificate_id": cert["certificate_id"],
                "host": cert["host"],
                "quantum_score": cert.get("quantum_attestation", {}).get("quantum_score", 0),
                "status": cert.get("status", "unknown"),
                "issued_at": cert.get("issued_at", ""),
                "expires_at": cert.get("validity", {}).get("not_after", ""),
            }
            for cert in self._certificates.values()
        ]

    def _anchor_to_blockchain(self, cert_id: str, cert_hash: str, timestamp: datetime) -> Dict:
        """
        Simulate blockchain anchoring by appending to a hash-chained ledger.
        Each block references the previous block's hash (simple blockchain).
        """
        prev_hash = self._ledger[-1]["block_hash"] if self._ledger else "0" * 64

        block_data = f"{cert_id}|{cert_hash}|{prev_hash}|{timestamp.isoformat()}"
        block_hash = hashlib.sha3_256(block_data.encode()).hexdigest()
        tx_hash = hashlib.sha3_256(f"tx:{cert_id}:{cert_hash}".encode()).hexdigest()

        block = {
            "block_number": len(self._ledger) + 1,
            "tx_hash": tx_hash,
            "block_hash": block_hash,
            "prev_hash": prev_hash,
            "certificate_id": cert_id,
            "certificate_hash": cert_hash,
            "timestamp": timestamp.isoformat(),
            "network": "qsentra-ledger",
            "consensus": "simulated-pbft",
        }

        self._ledger.append(block)

        return {
            "tx_hash": tx_hash,
            "block_number": block["block_number"],
            "block_hash": block_hash,
            "network": "Q-Sentra Ledger (Hyperledger Fabric Simulated)",
            "anchored_at": timestamp.isoformat(),
        }

    def _detect_pqc_algos(self, scan: Dict) -> List[str]:
        """Detect PQC algorithms in use."""
        algos = []
        kex = scan.get("key_exchange", "")
        sig = scan.get("signature_algorithm", "")
        if "ML-KEM" in kex or "Kyber" in kex:
            algos.append(kex)
        if "ML-DSA" in sig or "SLH-DSA" in sig:
            algos.append(sig)
        return algos

    def get_ledger(self) -> List[Dict]:
        """Return the full blockchain ledger for auditing."""
        return self._ledger
