import ssl
import socket
from datetime import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519, ed448, dsa

class TLSScanner:
    def __init__(self, hostname: str, port: int = 443):
        self.hostname = hostname
        self.port = port
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def scan(self) -> dict:
        try:
            with socket.create_connection((self.hostname, self.port), timeout=10) as sock:
                with self.ctx.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert_bin = ssock.getpeercert(binary_form=True)
                    cipher = ssock.cipher()
                    tls_version = ssock.version()

            if not cert_bin:
                return {}

            cert = x509.load_der_x509_certificate(cert_bin, default_backend())
            
            # Extract basic info
            subject_str = ",".join([f"{n.oid._name}={n.value}" for n in cert.subject])
            issuer_str = ",".join([f"{n.oid._name}={n.value}" for n in cert.issuer])
            
            # Key algorithms
            public_key = cert.public_key()
            key_algorithm = "Unknown"
            key_size = 0
            if isinstance(public_key, rsa.RSAPublicKey):
                key_algorithm = "RSA"
                key_size = public_key.key_size
            elif isinstance(public_key, ec.EllipticCurvePublicKey):
                key_algorithm = "ECDSA"
                key_size = public_key.curve.key_size
            elif isinstance(public_key, dsa.DSAPublicKey):
                key_algorithm = "DSA"
                key_size = public_key.key_size
            elif isinstance(public_key, (ed25519.Ed25519PublicKey, ed448.Ed448PublicKey)):
                key_algorithm = "EdDSA"
                key_size = 256
            
            certificate_chain = [{
                "subject": subject_str,
                "issuer": issuer_str,
                "valid_from": cert.not_valid_before.isoformat(),
                "valid_to": cert.not_valid_after.isoformat(),
                "signature_algorithm": cert.signature_hash_algorithm.name if cert.signature_hash_algorithm else "Unknown",
                "public_key": {
                    "algorithm": key_algorithm,
                    "size": key_size
                }
            }]
            
            mechanism = "RSA"
            curve = "none"
            cipher_name = cipher[0] if cipher else ""
            if "ECDHE" in cipher_name:
                mechanism = "ECDHE"
                curve = "secp256r1"
            elif "DHE" in cipher_name:
                mechanism = "DHE"
            
            return {
                "hostname": self.hostname,
                "scan_timestamp": datetime.utcnow().isoformat() + "Z",
                "certificate_chain": certificate_chain,
                "tls_version": tls_version,
                "cipher_suite": cipher_name,
                "key_exchange": {
                    "mechanism": mechanism,
                    "curve": curve
                }
            }
        except Exception as e:
            return {"error": str(e), "hostname": self.hostname}
