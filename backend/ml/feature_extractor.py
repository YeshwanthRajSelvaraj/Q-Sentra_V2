"""Feature Extractor for PQC Scoring."""
from datetime import datetime, timezone

def extract_features(cbom_json: dict) -> dict:
    """
    Extract features for ML model from CBOM JSON.
    """
    features = {}
    
    # Defaults
    features["sig_sha256_rsa"] = 0
    features["sig_sha384_ecdsa"] = 0
    features["sig_sha256_ecdsa"] = 0
    features["sig_sha1_rsa"] = 0

    features["pk_rsa"] = 0
    features["pk_ecdsa"] = 0
    features["pk_eddsa"] = 0
    features["pk_dsa"] = 0

    features["kex_rsa"] = 0
    features["kex_ecdhe"] = 0
    features["kex_dhe"] = 0
    features["kex_psk"] = 0

    features["tls_1_0"] = 0
    features["tls_1_1"] = 0
    features["tls_1_2"] = 0
    features["tls_1_3"] = 0

    features["curve_secp256r1"] = 0
    features["curve_secp384r1"] = 0
    features["curve_x25519"] = 0
    features["curve_none"] = 1

    features["key_size"] = 2048
    features["cert_validity_days"] = 365
    features["chain_length"] = 1
    features["days_until_expiry"] = 90
    
    features["supports_pqc"] = 0
    features["uses_modern_tls_1_3"] = 0
    features["uses_weak_signature"] = 0
    
    if not cbom_json:
        return features

    # TLS Version
    tls_version = cbom_json.get("tls_version", "")
    if "1.3" in tls_version:
        features["tls_1_3"] = 1
        features["uses_modern_tls_1_3"] = 1
    elif "1.2" in tls_version:
        features["tls_1_2"] = 1
    elif "1.1" in tls_version:
        features["tls_1_1"] = 1
    elif "1.0" in tls_version:
        features["tls_1_0"] = 1

    kex = cbom_json.get("key_exchange", {})
    mech = kex.get("mechanism", "")
    if mech == "RSA": features["kex_rsa"] = 1
    elif mech == "ECDHE": features["kex_ecdhe"] = 1
    elif mech == "DHE": features["kex_dhe"] = 1
    elif mech == "PSK": features["kex_psk"] = 1
    
    curve = kex.get("curve", "")
    if curve == "secp256r1":
        features["curve_secp256r1"] = 1
        features["curve_none"] = 0
    elif curve == "secp384r1":
        features["curve_secp384r1"] = 1
        features["curve_none"] = 0
    elif curve == "X25519":
        features["curve_x25519"] = 1
        features["curve_none"] = 0

    chain = cbom_json.get("certificate_chain", [])
    features["chain_length"] = len(chain)
    
    if chain:
        cert = chain[0]
        pk = cert.get("public_key", {})
        algo = pk.get("algorithm", "")
        if algo == "RSA": features["pk_rsa"] = 1
        elif algo == "ECDSA": features["pk_ecdsa"] = 1
        elif algo == "EdDSA": features["pk_eddsa"] = 1
        elif algo == "DSA": features["pk_dsa"] = 1
        
        features["key_size"] = pk.get("size", 2048)
        
        sig = cert.get("signature_algorithm", "")
        if "sha256WithRSA" in sig or "sha256WithRSAEncryption" in sig: features["sig_sha256_rsa"] = 1
        elif "ecdsa-with-SHA384" in sig: features["sig_sha384_ecdsa"] = 1
        elif "ecdsa-with-SHA256" in sig: features["sig_sha256_ecdsa"] = 1
        elif "sha1" in sig.lower() or "md5" in sig.lower():
            features["sig_sha1_rsa"] = 1
            features["uses_weak_signature"] = 1
            
        try:
            valid_from = datetime.fromisoformat(cert.get("valid_from", "").replace("Z","+00:00"))
            valid_to = datetime.fromisoformat(cert.get("valid_to", "").replace("Z","+00:00"))
            features["cert_validity_days"] = (valid_to - valid_from).days
            features["days_until_expiry"] = (valid_to - datetime.now(timezone.utc)).days
        except Exception:
            pass

    return features
