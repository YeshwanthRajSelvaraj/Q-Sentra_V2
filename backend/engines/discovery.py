"""
Q-Sentra Discovery Engine
Discovers cryptographic assets using:
  - crt.sh API (Certificate Transparency logs)
  - DNS enumeration (subfinder-like logic)
  - Shodan/Censys (mock API)

Usage:
    engine = DiscoveryEngine()
    results = await engine.discover("pnb.co.in")
"""
import asyncio
import socket
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("qsentra.discovery")


class DiscoveryEngine:
    """Discovers public-facing cryptographic assets for a given domain."""

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self._common_subdomains = [
            "www", "mail", "api", "vpn", "cdn", "portal", "admin",
            "netbanking", "mobile", "upi", "imps", "swift", "neft",
            "rtgs", "crm", "hrms", "treasury", "forex", "loan",
            "insurance", "cards", "pos", "atm", "branch", "kyc",
            "sso", "auth", "siem", "grafana", "jenkins",
        ]

    async def discover(self, domain: str) -> Dict:
        """
        Run full discovery pipeline for a domain.
        Returns dict with discovered assets from all sources.
        """
        logger.info(f"Starting discovery for domain: {domain}")
        start_time = datetime.now(timezone.utc)

        # Run all discovery methods concurrently
        ct_task = asyncio.create_task(self.query_crt_sh(domain))
        dns_task = asyncio.create_task(self.dns_enumerate(domain))
        osint_task = asyncio.create_task(self.osint_scan(domain))

        ct_results = await ct_task
        dns_results = await dns_task
        osint_results = await osint_task

        # Merge and deduplicate
        all_domains = set()
        for result in ct_results + dns_results + osint_results:
            all_domains.add(result["domain"])

        # Resolve IPs for all discovered domains
        assets = []
        for subdomain in all_domains:
            ip = await self._resolve_ip(subdomain)
            assets.append({
                "domain": subdomain,
                "ip": ip or "unresolved",
                "port": 443,
                "source": self._get_source(subdomain, ct_results, dns_results, osint_results),
                "discovered_at": datetime.now(timezone.utc).isoformat(),
                "status": "new",
            })

        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        logger.info(f"Discovery complete for {domain}: {len(assets)} assets in {elapsed:.1f}s")

        return {
            "domain": domain,
            "total_assets": len(assets),
            "sources": {
                "ct_logs": len(ct_results),
                "dns_enum": len(dns_results),
                "osint": len(osint_results),
            },
            "assets": assets,
            "scan_time_seconds": elapsed,
            "timestamp": start_time.isoformat(),
        }

    async def query_crt_sh(self, domain: str) -> List[Dict]:
        """
        Query crt.sh Certificate Transparency API for subdomains.
        This is a REAL API call to crt.sh.
        """
        results = []
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    seen = set()
                    for entry in data:
                        name = entry.get("name_value", "")
                        # crt.sh can return wildcard or multi-line names
                        for sub_name in name.split("\n"):
                            sub_name = sub_name.strip().lstrip("*.")
                            if sub_name and sub_name.endswith(domain) and sub_name not in seen:
                                seen.add(sub_name)
                                results.append({
                                    "domain": sub_name,
                                    "source": "crt.sh",
                                    "issuer": entry.get("issuer_name", ""),
                                    "not_after": entry.get("not_after", ""),
                                    "entry_timestamp": entry.get("entry_timestamp", ""),
                                })
                    logger.info(f"crt.sh returned {len(results)} unique subdomains for {domain}")
                else:
                    logger.warning(f"crt.sh returned status {response.status_code}")
        except Exception as e:
            logger.error(f"crt.sh query failed: {e}")
            # Fallback to mock data for demo
            results = self._mock_ct_results(domain)
        return results

    async def dns_enumerate(self, domain: str) -> List[Dict]:
        """
        DNS brute-force enumeration using common subdomain wordlist.
        Resolves each potential subdomain to check existence.
        """
        results = []
        tasks = []

        for sub in self._common_subdomains:
            fqdn = f"{sub}.{domain}"
            tasks.append(self._check_subdomain(fqdn))

        resolved = await asyncio.gather(*tasks, return_exceptions=True)
        for sub, result in zip(self._common_subdomains, resolved):
            if isinstance(result, str) and result:
                fqdn = f"{sub}.{domain}"
                results.append({
                    "domain": fqdn,
                    "source": "dns_enum",
                    "ip": result,
                })

        logger.info(f"DNS enumeration found {len(results)} subdomains for {domain}")
        return results

    async def osint_scan(self, domain: str) -> List[Dict]:
        """
        Simulate Shodan/Censys OSINT scan.
        In production, this would call Shodan/Censys APIs with API keys.
        """
        # Mock OSINT results for demo
        mock_osint = [
            {"domain": f"staging.{domain}", "source": "shodan", "ports": [443, 8443]},
            {"domain": f"dev.{domain}", "source": "shodan", "ports": [443]},
            {"domain": f"test.{domain}", "source": "censys", "ports": [443, 80]},
            {"domain": f"backup.{domain}", "source": "censys", "ports": [443]},
        ]
        logger.info(f"OSINT scan returned {len(mock_osint)} results (mock)")
        return mock_osint

    async def _resolve_ip(self, domain: str) -> Optional[str]:
        """Resolve a domain name to its IP address."""
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, lambda: socket.gethostbyname(domain)
            )
            return result
        except (socket.gaierror, socket.timeout):
            return None

    async def _check_subdomain(self, fqdn: str) -> Optional[str]:
        """Check if a subdomain resolves and return its IP."""
        try:
            loop = asyncio.get_event_loop()
            ip = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: socket.gethostbyname(fqdn)),
                timeout=3.0,
            )
            return ip
        except (socket.gaierror, socket.timeout, asyncio.TimeoutError):
            return None

    def _get_source(self, domain, ct, dns, osint) -> str:
        """Determine the discovery source for a domain."""
        for r in ct:
            if r["domain"] == domain:
                return "ct_logs"
        for r in dns:
            if r["domain"] == domain:
                return "dns_enum"
        for r in osint:
            if r["domain"] == domain:
                return "osint"
        return "unknown"

    def _mock_ct_results(self, domain: str) -> List[Dict]:
        """Fallback mock CT log results when crt.sh is unreachable."""
        subs = ["www", "mail", "api", "netbanking", "mobile", "vpn",
                "upi", "portal", "cdn", "swift", "imps", "neft"]
        return [
            {
                "domain": f"{sub}.{domain}",
                "source": "crt.sh",
                "issuer": "C=US, O=DigiCert Inc, CN=DigiCert SHA2 Extended Validation Server CA",
                "not_after": "2027-06-15T23:59:59",
            }
            for sub in subs
        ]
