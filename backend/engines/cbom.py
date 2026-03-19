"""
Q-Sentra CBOM Generator
Generates CycloneDX 1.6 compliant Cryptographic Bill of Materials.
Stores results in MongoDB for versioned tracking.

The CBOM includes:
  - TLS configuration components
  - Certificate components
  - Key exchange algorithms
  - Signature algorithms
  - Identified vulnerabilities
"""
import uuid
import hashlib
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger("qsentra.cbom")


class CBOMGenerator:
    """Generates CycloneDX 1.6-style CBOM documents from scan results."""

    SPEC_VERSION = "1.6"
    SCHEMA = "https://cyclonedx.org/schema/bom-1.6.schema.json"

    # Cryptographic algorithm classifications
    ALGORITHM_CLASSES = {
        # Symmetric encryption
        "AES-256-GCM": {"type": "symmetric", "strength": "high", "quantum_safe": False, "nist_level": 5},
        "AES-128-GCM": {"type": "symmetric", "strength": "medium", "quantum_safe": False, "nist_level": 1},
        "CHACHA20-POLY1305": {"type": "symmetric", "strength": "high", "quantum_safe": False, "nist_level": 5},
        "AES-256-CBC": {"type": "symmetric", "strength": "medium", "quantum_safe": False, "nist_level": 5},
        "3DES": {"type": "symmetric", "strength": "weak", "quantum_safe": False, "nist_level": 0},
        "RC4": {"type": "symmetric", "strength": "broken", "quantum_safe": False, "nist_level": 0},
        # Key exchange
        "ECDHE": {"type": "key_exchange", "strength": "high", "quantum_safe": False},
        "DHE": {"type": "key_exchange", "strength": "medium", "quantum_safe": False},
        "RSA": {"type": "key_exchange", "strength": "low", "quantum_safe": False},
        "X25519": {"type": "key_exchange", "strength": "high", "quantum_safe": False},
        "ML-KEM-768": {"type": "key_exchange", "strength": "high", "quantum_safe": True},
        "ML-KEM-1024": {"type": "key_exchange", "strength": "very_high", "quantum_safe": True},
        "X25519+Kyber768": {"type": "key_exchange", "strength": "very_high", "quantum_safe": True},
        # Signatures
        "SHA256withRSA": {"type": "signature", "strength": "medium", "quantum_safe": False},
        "SHA384withECDSA": {"type": "signature", "strength": "high", "quantum_safe": False},
        "ML-DSA-65": {"type": "signature", "strength": "high", "quantum_safe": True},
        "ML-DSA-87": {"type": "signature", "strength": "very_high", "quantum_safe": True},
        "SLH-DSA-128f": {"type": "signature", "strength": "high", "quantum_safe": True},
    }

    def generate(self, asset_id: str, scan_result: Dict) -> Dict:
        """
        Generate a complete CycloneDX 1.6 CBOM from a scan result.

        Args:
            asset_id: Unique identifier for the asset
            scan_result: Output from CryptoScanner.scan()

        Returns:
            CycloneDX-compliant CBOM JSON document
        """
        serial = f"urn:uuid:{uuid.uuid4()}"
        host = scan_result.get("host", asset_id)
        components = []
        vulnerabilities = []

        # ── 1. TLS Protocol Component ──
        tls_version = scan_result.get("tls_version", "Unknown")
        components.append({
            "type": "cryptographic-asset",
            "bom-ref": f"tls-{asset_id}",
            "name": f"TLS Protocol ({tls_version})",
            "version": tls_version,
            "cryptoProperties": {
                "assetType": "protocol",
                "protocolProperties": {
                    "type": "tls",
                    "version": tls_version,
                },
            },
            "evidence": {
                "occurrences": [{"location": f"{host}:443"}]
            },
        })

        # ── 2. Cipher Suite Component ──
        cipher = scan_result.get("cipher_suite", "Unknown")
        cipher_strength = self._classify_cipher(cipher)
        components.append({
            "type": "cryptographic-asset",
            "bom-ref": f"cipher-{asset_id}",
            "name": cipher,
            "cryptoProperties": {
                "assetType": "algorithm",
                "algorithmProperties": {
                    "primitive": "cipher",
                    "mode": self._extract_mode(cipher),
                    "keyLength": scan_result.get("cipher_bits", 0),
                    "cryptoFunctions": ["encrypt", "decrypt"],
                },
            },
            "properties": [
                {"name": "strength", "value": cipher_strength},
                {"name": "quantum_safe", "value": str(False)},
            ],
        })

        # ── 3. Key Exchange Component ──
        kex = scan_result.get("key_exchange", "Unknown")
        kex_info = self.ALGORITHM_CLASSES.get(kex, {"type": "key_exchange", "strength": "unknown", "quantum_safe": False})
        components.append({
            "type": "cryptographic-asset",
            "bom-ref": f"kex-{asset_id}",
            "name": f"Key Exchange: {kex}",
            "cryptoProperties": {
                "assetType": "algorithm",
                "algorithmProperties": {
                    "primitive": "key-agree",
                    "cryptoFunctions": ["keygen"],
                },
            },
            "properties": [
                {"name": "strength", "value": kex_info["strength"]},
                {"name": "quantum_safe", "value": str(kex_info["quantum_safe"])},
                {"name": "provides_pfs", "value": str(kex in ("ECDHE", "DHE", "X25519", "ML-KEM-768", "ML-KEM-1024"))},
            ],
        })

        # ── 4. Signature Algorithm Component ──
        sig_algo = scan_result.get("signature_algorithm", "Unknown")
        components.append({
            "type": "cryptographic-asset",
            "bom-ref": f"sig-{asset_id}",
            "name": f"Signature: {sig_algo}",
            "cryptoProperties": {
                "assetType": "algorithm",
                "algorithmProperties": {
                    "primitive": "signature",
                    "cryptoFunctions": ["sign", "verify"],
                },
            },
            "properties": [
                {"name": "quantum_safe", "value": str(any(pqc in sig_algo for pqc in ("ML-DSA", "SLH-DSA")))},
            ],
        })

        # ── 5. Certificate Component ──
        cert = scan_result.get("certificate", {})
        if cert:
            components.append({
                "type": "cryptographic-asset",
                "bom-ref": f"cert-{asset_id}",
                "name": f"X.509 Certificate ({cert.get('key_type', 'Unknown')} {cert.get('key_bits', '?')}-bit)",
                "cryptoProperties": {
                    "assetType": "certificate",
                    "certificateProperties": {
                        "subjectName": str(cert.get("subject", {})),
                        "issuerName": str(cert.get("issuer", {})),
                        "notValidBefore": cert.get("not_before", ""),
                        "notValidAfter": cert.get("not_after", ""),
                        "signatureAlgorithm": sig_algo,
                    },
                },
                "properties": [
                    {"name": "key_type", "value": cert.get("key_type", "Unknown")},
                    {"name": "key_bits", "value": str(cert.get("key_bits", 0))},
                    {"name": "fingerprint_sha256", "value": cert.get("fingerprint_sha256", "")},
                    {"name": "is_expired", "value": str(cert.get("is_expired", False))},
                    {"name": "self_signed", "value": str(cert.get("self_signed", False))},
                ],
            })

        # ── 6. Vulnerability Mapping ──
        for vuln_str in scan_result.get("vulnerabilities", []):
            vuln_id = f"QSENTRA-{hashlib.md5(vuln_str.encode()).hexdigest()[:8].upper()}"
            severity = "critical" if any(w in vuln_str for w in ("WEAK_CIPHER", "EXPIRED", "WEAK_KEY")) else \
                       "high" if "QUANTUM" in vuln_str or "LEGACY" in vuln_str else "medium"
            vulnerabilities.append({
                "id": vuln_id,
                "source": {"name": "Q-Sentra Scanner"},
                "description": vuln_str,
                "ratings": [{"severity": severity, "method": "other"}],
                "affects": [{"ref": f"tls-{asset_id}"}],
                "recommendation": self._get_recommendation(vuln_str),
            })

        # ── Assemble CBOM ──
        cbom = {
            "$schema": self.SCHEMA,
            "bomFormat": "CycloneDX",
            "specVersion": self.SPEC_VERSION,
            "serialNumber": serial,
            "version": 1,
            "metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "tools": [{
                    "vendor": "Q-Sentra",
                    "name": "Q-Sentra Cryptographic Scanner",
                    "version": "1.0.0",
                }],
                "component": {
                    "type": "application",
                    "name": host,
                    "bom-ref": asset_id,
                },
            },
            "components": components,
            "vulnerabilities": vulnerabilities,
            "compositions": [{
                "aggregate": "complete",
                "assemblies": [c["bom-ref"] for c in components],
            }],
        }

        # Add asset_id for MongoDB storage
        cbom["asset_id"] = asset_id
        cbom["host"] = host

        logger.info(f"Generated CBOM for {host}: {len(components)} components, {len(vulnerabilities)} vulnerabilities")
        return cbom

    def _classify_cipher(self, cipher: str) -> str:
        """Classify cipher suite strength."""
        cipher_upper = cipher.upper()
        if any(w in cipher_upper for w in ("RC4", "DES", "NULL", "EXPORT")):
            return "broken"
        if "CBC" in cipher_upper or "SHA1" in cipher_upper:
            return "weak"
        if "GCM" in cipher_upper or "CHACHA" in cipher_upper:
            return "strong"
        return "medium"

    def _extract_mode(self, cipher: str) -> str:
        """Extract encryption mode from cipher name."""
        for mode in ("GCM", "CBC", "CCM", "CTR"):
            if mode in cipher.upper():
                return mode
        return "stream" if "CHACHA" in cipher.upper() else "unknown"

    def _get_recommendation(self, vuln: str) -> str:
        """Generate remediation recommendation for a vulnerability."""
        if "WEAK_CIPHER" in vuln:
            return "Upgrade to AES-256-GCM or CHACHA20-POLY1305."
        if "LEGACY_TLS" in vuln:
            return "Disable TLS 1.0/1.1 and enforce TLS 1.2+ with strong cipher suites."
        if "NO_PFS" in vuln:
            return "Switch to ECDHE or DHE key exchange for Perfect Forward Secrecy."
        if "QUANTUM" in vuln:
            return "Plan migration to ML-KEM-768 (FIPS 203) for quantum-safe key exchange."
        if "EXPIRED" in vuln:
            return "Renew the expired certificate immediately."
        if "WEAK_KEY" in vuln:
            return "Generate new RSA key with minimum 2048-bit length, prefer 3072+."
        return "Review and remediate according to organizational security policy."

    def to_xml(self, cbom: Dict) -> str:
        """Convert CBOM JSON to CycloneDX XML format (simplified)."""
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append(f'<bom xmlns="http://cyclonedx.org/schema/bom/1.6" version="1" serialNumber="{cbom["serialNumber"]}">')
        lines.append("  <components>")
        for comp in cbom.get("components", []):
            lines.append(f'    <component type="{comp["type"]}" bom-ref="{comp["bom-ref"]}">')
            lines.append(f'      <name>{comp["name"]}</name>')
            lines.append("    </component>")
        lines.append("  </components>")
        lines.append("</bom>")
        return "\n".join(lines)
