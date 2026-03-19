"""
Q-Sentra PQC Validation Engine
Computes Quantum-Safety Score (0-100) for cryptographic assets
based on NIST Post-Quantum Cryptography standards.

Scoring dimensions:
  1. TLS version (25 pts)
  2. Key exchange algorithm (25 pts)
  3. Cipher suite strength (20 pts)
  4. Certificate key strength (15 pts)
  5. Forward secrecy and PQC readiness (15 pts)
"""
import logging
from typing import Dict, Tuple

logger = logging.getLogger("qsentra.pqc")


class PQCValidator:
    """Validates cryptographic configurations against NIST PQC standards."""

    # ── TLS Version Scoring (max 25) ──
    TLS_SCORES = {
        "TLSv1.3": 25,
        "TLSv1.2": 15,
        "TLSv1.1": 5,
        "TLSv1.0": 0,
        "SSLv3": 0,
    }

    # ── Key Exchange Scoring (max 25) ──
    KEX_SCORES = {
        # PQC algorithms (highest scores)
        "ML-KEM-1024": 25,
        "ML-KEM-768": 24,
        "X25519+Kyber768": 23,
        # Classical algorithms
        "X25519": 15,
        "ECDHE": 14,
        "DHE": 10,
        "ECDH": 8,
        "DH": 5,
        "RSA": 2,
    }

    # ── Cipher Suite Scoring (max 20) ──
    CIPHER_SCORES = {
        "CHACHA20-POLY1305": 20,
        "AES-256-GCM": 20,
        "AES-128-GCM": 16,
        "AES-256-CBC": 10,
        "AES-128-CBC": 8,
        "3DES": 2,
        "RC4": 0,
        "DES": 0,
        "NULL": 0,
    }

    # ── Signature Algorithm Scoring (max bonus within PQC) ──
    SIG_SCORES = {
        "ML-DSA-87": 15,
        "ML-DSA-65": 14,
        "SLH-DSA-128f": 13,
        "SLH-DSA-192f": 13,
        "SHA384withECDSA": 8,
        "SHA256withRSA": 5,
        "SHA1withRSA": 0,
    }

    # NIST PQC Standards reference
    NIST_STANDARDS = {
        "FIPS 203": {
            "name": "Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM)",
            "algorithms": ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"],
            "status": "Finalized (August 2024)",
        },
        "FIPS 204": {
            "name": "Module-Lattice-Based Digital Signature Algorithm (ML-DSA)",
            "algorithms": ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"],
            "status": "Finalized (August 2024)",
        },
        "FIPS 205": {
            "name": "Stateless Hash-Based Digital Signature Algorithm (SLH-DSA)",
            "algorithms": ["SLH-DSA-128f", "SLH-DSA-128s", "SLH-DSA-192f", "SLH-DSA-192s", "SLH-DSA-256f", "SLH-DSA-256s"],
            "status": "Finalized (August 2024)",
        },
    }

    # Risk category thresholds
    RISK_THRESHOLDS = {
        (90, 101): "minimal",
        (70, 90): "low",
        (50, 70): "medium",
        (30, 50): "high",
        (0, 30): "critical",
    }

    def validate(self, scan_result: Dict) -> Dict:
        """
        Compute comprehensive quantum-safety score for an asset.

        Args:
            scan_result: Output from CryptoScanner.scan()

        Returns:
            Dict with score, risk_category, breakdown, and recommendations
        """
        host = scan_result.get("host", "unknown")
        breakdown = {}
        recommendations = []

        # ── 1. TLS Version Score ──
        tls = scan_result.get("tls_version", "Unknown")
        tls_score = self.TLS_SCORES.get(tls, 0)
        breakdown["tls_version"] = {
            "value": tls,
            "score": tls_score,
            "max": 25,
            "weight": "25%",
        }
        if tls_score < 25:
            recommendations.append({
                "priority": "high" if tls_score < 15 else "medium",
                "action": f"Upgrade from {tls} to TLS 1.3",
                "impact": f"+{25 - tls_score} points",
            })

        # ── 2. Key Exchange Score ──
        kex = scan_result.get("key_exchange", "Unknown")
        kex_score = self._score_kex(kex)
        breakdown["key_exchange"] = {
            "value": kex,
            "score": kex_score,
            "max": 25,
            "weight": "25%",
        }
        if kex_score < 20:
            target = "ML-KEM-768 (FIPS 203)" if kex_score < 15 else "X25519+Kyber768 (Hybrid)"
            recommendations.append({
                "priority": "critical" if kex_score < 10 else "high",
                "action": f"Migrate key exchange from {kex} to {target}",
                "impact": f"+{25 - kex_score} points",
                "nist_reference": "FIPS 203",
            })

        # ── 3. Cipher Suite Score ──
        cipher = scan_result.get("cipher_suite", "Unknown")
        cipher_score = self._score_cipher(cipher)
        breakdown["cipher_suite"] = {
            "value": cipher,
            "score": cipher_score,
            "max": 20,
            "weight": "20%",
        }
        if cipher_score < 16:
            recommendations.append({
                "priority": "high" if cipher_score < 10 else "medium",
                "action": f"Upgrade cipher to AES-256-GCM or CHACHA20-POLY1305",
                "impact": f"+{20 - cipher_score} points",
            })

        # ── 4. Certificate Key Strength ──
        cert = scan_result.get("certificate", {})
        cert_score = self._score_certificate(cert)
        breakdown["certificate"] = {
            "key_type": cert.get("key_type", "Unknown"),
            "key_bits": cert.get("key_bits", 0),
            "score": cert_score,
            "max": 15,
            "weight": "15%",
        }
        if cert_score < 12:
            recommendations.append({
                "priority": "medium",
                "action": f"Upgrade certificate key to RSA-3072+ or ECDSA P-384",
                "impact": f"+{15 - cert_score} points",
            })

        # ── 5. PQC Readiness Score ──
        pqc_score = self._score_pqc_readiness(scan_result)
        breakdown["pqc_readiness"] = {
            "score": pqc_score,
            "max": 15,
            "weight": "15%",
            "details": self._get_pqc_details(scan_result),
        }
        if pqc_score < 10:
            recommendations.append({
                "priority": "critical",
                "action": "Implement post-quantum cryptographic algorithms (FIPS 203/204/205)",
                "impact": f"+{15 - pqc_score} points",
                "timeline": "Within 12 months",
            })

        # ── Calculate Total Score ──
        total_score = min(100, tls_score + kex_score + cipher_score + cert_score + pqc_score)
        risk_category = self._get_risk_category(total_score)

        # ── HNDL (Harvest Now, Decrypt Later) Risk ──
        hndl_risk = self._calculate_hndl_risk(scan_result, total_score)

        result = {
            "host": host,
            "quantum_score": total_score,
            "risk_category": risk_category,
            "breakdown": breakdown,
            "recommendations": sorted(recommendations, key=lambda r: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(r["priority"], 4)),
            "hndl_risk": hndl_risk,
            "nist_standards": self.NIST_STANDARDS,
            "validated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        }

        logger.info(f"PQC validation for {host}: score={total_score}, risk={risk_category}")
        return result

    def _score_kex(self, kex: str) -> int:
        """Score key exchange algorithm."""
        if kex in self.KEX_SCORES:
            return self.KEX_SCORES[kex]
        # Partial match
        for name, score in self.KEX_SCORES.items():
            if name.lower() in kex.lower():
                return score
        return 0

    def _score_cipher(self, cipher: str) -> int:
        """Score cipher suite."""
        cipher_upper = cipher.upper()
        for name, score in self.CIPHER_SCORES.items():
            if name.replace("-", "").upper() in cipher_upper.replace("-", "").replace("_", ""):
                return score
        if "GCM" in cipher_upper:
            return 16
        if "CBC" in cipher_upper:
            return 8
        return 5

    def _score_certificate(self, cert: Dict) -> int:
        """Score certificate key strength."""
        key_type = cert.get("key_type", "")
        key_bits = cert.get("key_bits", 0)

        if cert.get("is_expired"):
            return 0

        if key_type == "RSA":
            if key_bits >= 4096:
                return 15
            elif key_bits >= 3072:
                return 13
            elif key_bits >= 2048:
                return 10
            else:
                return 3
        elif key_type in ("EC", "ECDSA"):
            if key_bits >= 384:
                return 15
            elif key_bits >= 256:
                return 13
            else:
                return 8
        return 5

    def _score_pqc_readiness(self, scan: Dict) -> int:
        """Score post-quantum cryptography readiness."""
        score = 0
        kex = scan.get("key_exchange", "")
        sig = scan.get("signature_algorithm", "")
        tls = scan.get("tls_version", "")

        # PQC key exchange
        if kex in ("ML-KEM-768", "ML-KEM-1024", "X25519+Kyber768"):
            score += 8
        elif kex in ("X25519", "ECDHE"):
            score += 3  # Upgradeable

        # PQC signature
        if any(pqc in sig for pqc in ("ML-DSA", "SLH-DSA")):
            score += 5
        elif "ECDSA" in sig or "sha384" in sig.lower():
            score += 2

        # TLS 1.3 (required base for PQC)
        if "1.3" in tls:
            score += 2

        return min(15, score)

    def _get_risk_category(self, score: int) -> str:
        """Map score to risk category."""
        for (low, high), category in self.RISK_THRESHOLDS.items():
            if low <= score < high:
                return category
        return "critical"

    def _calculate_hndl_risk(self, scan: Dict, score: int) -> Dict:
        """
        Calculate Harvest Now, Decrypt Later risk.
        Estimates years until a CRQC could break current encryption.
        """
        kex = scan.get("key_exchange", "")
        cert = scan.get("certificate", {})
        key_bits = cert.get("key_bits", 2048)
        key_type = cert.get("key_type", "RSA")

        # Estimated years to CRQC breaking (conservative)
        if kex in ("ML-KEM-768", "ML-KEM-1024"):
            years_to_break = 50  # Quantum resistant
        elif key_type == "RSA":
            if key_bits >= 4096:
                years_to_break = 8
            elif key_bits >= 3072:
                years_to_break = 6
            elif key_bits >= 2048:
                years_to_break = 4
            else:
                years_to_break = 1
        elif key_type in ("EC", "ECDSA"):
            years_to_break = 5 if key_bits >= 256 else 2
        else:
            years_to_break = 3

        # Risk score (higher = worse)
        hndl_score = max(0, 100 - score - (years_to_break * 5))

        return {
            "hndl_risk_score": round(hndl_score, 1),
            "estimated_years_to_crqc": years_to_break,
            "data_sensitivity": "high" if "banking" in scan.get("host", "").lower() or "payment" in scan.get("host", "").lower() else "medium",
            "recommendation": "Immediate PQC migration required" if hndl_score > 70 else
                            "Plan PQC migration within 12 months" if hndl_score > 40 else
                            "Monitor and plan for PQC transition" if hndl_score > 10 else
                            "Currently quantum-safe",
        }

    def _get_pqc_details(self, scan: Dict) -> Dict:
        """Get detailed PQC readiness information."""
        kex = scan.get("key_exchange", "")
        sig = scan.get("signature_algorithm", "")
        return {
            "has_pqc_kex": kex in ("ML-KEM-768", "ML-KEM-1024", "X25519+Kyber768"),
            "has_pqc_sig": any(p in sig for p in ("ML-DSA", "SLH-DSA")),
            "current_kex": kex,
            "current_sig": sig,
            "target_kex": "ML-KEM-768 (FIPS 203)",
            "target_sig": "ML-DSA-65 (FIPS 204)",
        }
