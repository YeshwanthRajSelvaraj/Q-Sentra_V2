"""
Q-Sentra Remediation Orchestrator
Generates actionable remediation playbooks based on scan results and PQC validation.

Outputs:
  - Nginx/Apache configuration fixes
  - TLS upgrade suggestions
  - Markdown playbook
  - YAML (Ansible-style) playbook
"""
import logging
from typing import Dict, List
from datetime import datetime, timezone

logger = logging.getLogger("qsentra.remediation")


class RemediationOrchestrator:
    """Generates remediation playbooks and configuration fixes."""

    # ── Nginx TLS Configuration Templates ──
    NGINX_TLS13 = """# Q-Sentra Generated - TLS 1.3 Hardened Configuration for {host}
# Generated: {timestamp}

server {{
    listen 443 ssl http2;
    server_name {host};

    # ── TLS 1.3 Only ──
    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers off;

    # ── Certificate ──
    ssl_certificate /etc/ssl/certs/{host}.pem;
    ssl_certificate_key /etc/ssl/private/{host}.key;

    # ── OCSP Stapling ──
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;

    # ── Session Tickets ──
    ssl_session_tickets off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;

    # ── HSTS ──
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # ── Security Headers ──
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    # ── PQC Key Exchange (when supported) ──
    # ssl_ecdh_curve X25519:P-384:P-256;
    # Future: ssl_conf_command Groups kyber768:x25519

    location / {{
        proxy_pass http://backend;
    }}
}}
"""

    NGINX_TLS12_UPGRADE = """# Q-Sentra Generated - TLS 1.2+ Configuration for {host}
# Transition configuration - upgrade to TLS 1.3 when possible

server {{
    listen 443 ssl http2;
    server_name {host};

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers on;

    ssl_certificate /etc/ssl/certs/{host}.pem;
    ssl_certificate_key /etc/ssl/private/{host}.key;

    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_session_tickets off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
}}
"""

    # ── Apache Configuration Template ──
    APACHE_TLS = """# Q-Sentra Generated - Apache TLS Configuration for {host}
# Generated: {timestamp}

<VirtualHost *:443>
    ServerName {host}

    SSLEngine on
    SSLProtocol -all +TLSv1.3 +TLSv1.2
    SSLCipherSuite TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder on

    SSLCertificateFile /etc/ssl/certs/{host}.pem
    SSLCertificateKeyFile /etc/ssl/private/{host}.key

    SSLUseStapling On
    SSLStaplingResponderTimeout 5
    SSLStaplingReturnResponderErrors off

    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
</VirtualHost>

SSLStaplingCache shmcb:/var/run/ocsp(128000)
"""

    def generate(self, host: str, scan_result: Dict, pqc_result: Dict) -> Dict:
        """
        Generate complete remediation package for an asset.

        Args:
            host: Target hostname
            scan_result: Output from CryptoScanner.scan()
            pqc_result: Output from PQCValidator.validate()

        Returns:
            Dict with configs, markdown playbook, and Ansible YAML
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        score = pqc_result.get("quantum_score", 0)
        recommendations = pqc_result.get("recommendations", [])
        vulns = scan_result.get("vulnerabilities", [])

        # Determine remediation complexity
        if score >= 90:
            complexity = "low"
            estimated_hours = 2
        elif score >= 70:
            complexity = "medium"
            estimated_hours = 8
        elif score >= 50:
            complexity = "high"
            estimated_hours = 24
        else:
            complexity = "critical"
            estimated_hours = 48

        # Generate all outputs
        result = {
            "host": host,
            "current_score": score,
            "target_score": 95,
            "complexity": complexity,
            "estimated_hours": estimated_hours,
            "configs": {
                "nginx": self._generate_nginx(host, scan_result, timestamp),
                "apache": self.APACHE_TLS.format(host=host, timestamp=timestamp),
            },
            "playbook_markdown": self._generate_markdown_playbook(host, scan_result, pqc_result, timestamp),
            "playbook_ansible": self._generate_ansible_playbook(host, scan_result, pqc_result),
            "tasks": self._generate_task_list(host, recommendations, vulns),
            "generated_at": timestamp,
        }

        logger.info(f"Generated remediation for {host}: complexity={complexity}, tasks={len(result['tasks'])}")
        return result

    def _generate_nginx(self, host: str, scan: Dict, timestamp: str) -> str:
        """Generate appropriate Nginx configuration."""
        tls = scan.get("tls_version", "")
        if "1.3" in tls:
            return self.NGINX_TLS13.format(host=host, timestamp=timestamp)
        return self.NGINX_TLS12_UPGRADE.format(host=host, timestamp=timestamp)

    def _generate_markdown_playbook(self, host: str, scan: Dict, pqc: Dict, timestamp: str) -> str:
        """Generate a comprehensive remediation playbook in Markdown."""
        score = pqc.get("quantum_score", 0)
        recommendations = pqc.get("recommendations", [])
        hndl = pqc.get("hndl_risk", {})

        lines = [
            f"# Q-Sentra Remediation Playbook",
            f"## Asset: {host}",
            f"",
            f"**Generated:** {timestamp}",
            f"**Current Quantum Score:** {score}/100",
            f"**Risk Category:** {pqc.get('risk_category', 'Unknown')}",
            f"**HNDL Risk Score:** {hndl.get('hndl_risk_score', 'N/A')}",
            f"",
            f"---",
            f"",
            f"## Current Configuration",
            f"",
            f"| Parameter | Current Value | Target Value |",
            f"|-----------|--------------|--------------|",
            f"| TLS Version | {scan.get('tls_version', 'Unknown')} | TLSv1.3 |",
            f"| Cipher Suite | {scan.get('cipher_suite', 'Unknown')} | TLS_AES_256_GCM_SHA384 |",
            f"| Key Exchange | {scan.get('key_exchange', 'Unknown')} | ML-KEM-768 (FIPS 203) |",
            f"| Signature | {scan.get('signature_algorithm', 'Unknown')} | ML-DSA-65 (FIPS 204) |",
            f"",
            f"---",
            f"",
            f"## Remediation Steps",
            f"",
        ]

        # Priority-ordered steps
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(rec.get("priority", ""), "⚪")
            lines.append(f"### Step {i}: {rec.get('action', 'TBD')}")
            lines.append(f"")
            lines.append(f"- **Priority:** {priority_emoji} {rec.get('priority', 'Unknown').upper()}")
            lines.append(f"- **Impact:** {rec.get('impact', 'TBD')}")
            if rec.get("nist_reference"):
                lines.append(f"- **NIST Reference:** {rec['nist_reference']}")
            if rec.get("timeline"):
                lines.append(f"- **Timeline:** {rec['timeline']}")
            lines.append(f"")

        # Add general best practices
        lines.extend([
            f"---",
            f"",
            f"## Verification",
            f"",
            f"After applying changes, verify with:",
            f"```bash",
            f"# Verify TLS configuration",
            f"openssl s_client -connect {host}:443 -tls1_3",
            f"",
            f"# Check cipher suites",
            f"nmap --script ssl-enum-ciphers -p 443 {host}",
            f"",
            f"# Re-scan with Q-Sentra",
            f"curl -X POST http://localhost:8000/scan/{host}",
            f"```",
            f"",
            f"---",
            f"*Generated by Q-Sentra Remediation Orchestrator v1.0*",
        ])

        return "\n".join(lines)

    def _generate_ansible_playbook(self, host: str, scan: Dict, pqc: Dict) -> str:
        """Generate Ansible-style YAML playbook."""
        score = pqc.get("quantum_score", 0)
        tls = scan.get("tls_version", "")

        playbook = f"""---
# Q-Sentra Ansible Playbook - TLS Hardening for {host}
# Current Score: {score}/100 | Target: 95/100

- name: "Q-Sentra TLS Hardening - {host}"
  hosts: "{host}"
  become: yes
  vars:
    target_host: "{host}"
    current_tls: "{tls}"
    target_tls: "TLSv1.3"
    ssl_cert_path: "/etc/ssl/certs/{host}.pem"
    ssl_key_path: "/etc/ssl/private/{host}.key"

  tasks:
    - name: "Phase 1 - Update OpenSSL to latest version"
      apt:
        name: openssl
        state: latest
      when: ansible_os_family == "Debian"

    - name: "Phase 2 - Generate new RSA-3072 key pair"
      openssl_privatekey:
        path: "{{{{ ssl_key_path }}}}"
        type: RSA
        size: 3072
      notify: restart_nginx

    - name: "Phase 3 - Generate CSR with strong parameters"
      openssl_csr:
        path: "/etc/ssl/certs/{{{{ target_host }}}}.csr"
        privatekey_path: "{{{{ ssl_key_path }}}}"
        common_name: "{{{{ target_host }}}}"
        organization_name: "Punjab National Bank"

    - name: "Phase 4 - Deploy TLS 1.3 Nginx configuration"
      template:
        src: "nginx_tls13.conf.j2"
        dest: "/etc/nginx/sites-enabled/{{{{ target_host }}}}.conf"
      notify: restart_nginx

    - name: "Phase 5 - Disable legacy TLS protocols"
      lineinfile:
        path: "/etc/nginx/nginx.conf"
        regexp: "ssl_protocols"
        line: "    ssl_protocols TLSv1.3;"
      notify: restart_nginx

    - name: "Phase 6 - Configure HSTS header"
      lineinfile:
        path: "/etc/nginx/sites-enabled/{{{{ target_host }}}}.conf"
        insertafter: "server_name"
        line: '    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;'
      notify: restart_nginx

    - name: "Phase 7 - Enable OCSP Stapling"
      blockinfile:
        path: "/etc/nginx/sites-enabled/{{{{ target_host }}}}.conf"
        insertafter: "ssl_certificate_key"
        block: |
          ssl_stapling on;
          ssl_stapling_verify on;
          resolver 8.8.8.8 8.8.4.4 valid=300s;
      notify: restart_nginx

    - name: "Phase 8 - Verify TLS configuration"
      command: "openssl s_client -connect {{{{ target_host }}}}:443 -tls1_3"
      register: tls_check
      failed_when: "'TLSv1.3' not in tls_check.stdout"

  handlers:
    - name: restart_nginx
      service:
        name: nginx
        state: restarted
"""
        return playbook

    def _generate_task_list(self, host: str, recommendations: List[Dict], vulns: List[str]) -> List[Dict]:
        """Generate structured task list for project management systems."""
        tasks = []

        # From recommendations
        for i, rec in enumerate(recommendations, 1):
            priority_map = {"critical": 1, "high": 2, "medium": 3, "low": 4}
            tasks.append({
                "id": f"REM-{host.split('.')[0].upper()}-{i:03d}",
                "title": rec.get("action", "Remediation task"),
                "priority": rec.get("priority", "medium"),
                "priority_order": priority_map.get(rec.get("priority", ""), 3),
                "status": "pending",
                "host": host,
                "impact": rec.get("impact", ""),
                "nist_reference": rec.get("nist_reference", ""),
                "estimated_hours": 4 if rec.get("priority") == "critical" else 2,
            })

        # From vulnerabilities
        for vuln in vulns:
            tasks.append({
                "id": f"VULN-{host.split('.')[0].upper()}-{len(tasks)+1:03d}",
                "title": f"Fix: {vuln.split(':')[0] if ':' in vuln else vuln}",
                "priority": "critical" if "WEAK" in vuln or "EXPIRED" in vuln else "high",
                "status": "pending",
                "host": host,
                "description": vuln,
            })

        return sorted(tasks, key=lambda t: t.get("priority_order", 3))
