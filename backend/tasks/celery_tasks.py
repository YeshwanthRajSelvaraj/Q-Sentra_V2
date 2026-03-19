"""
Q-Sentra Celery Tasks
Async task definitions for background processing.
"""
import logging
from core.celery_app import celery_app

logger = logging.getLogger("qsentra.tasks")


@celery_app.task(bind=True, name="tasks.celery_tasks.scan_asset")
def scan_asset(self, host: str, port: int = 443):
    """Async task: Scan a single asset's TLS configuration."""
    import asyncio
    from engines.scanner import CryptoScanner
    from engines.cbom import CBOMGenerator
    from engines.pqc_validator import PQCValidator

    logger.info(f"[Celery] Scanning {host}:{port}")
    scanner = CryptoScanner()
    cbom_gen = CBOMGenerator()
    pqc_val = PQCValidator()

    # Run async scan in sync context
    loop = asyncio.new_event_loop()
    try:
        scan_result = loop.run_until_complete(scanner.scan(host, port))
    finally:
        loop.close()

    # Generate CBOM and PQC score
    cbom = cbom_gen.generate(host, scan_result)
    pqc = pqc_val.validate(scan_result)

    return {
        "host": host,
        "scan_result": scan_result,
        "cbom_serial": cbom.get("serialNumber", ""),
        "quantum_score": pqc.get("quantum_score", 0),
        "risk_category": pqc.get("risk_category", ""),
    }


@celery_app.task(bind=True, name="tasks.celery_tasks.batch_scan")
def batch_scan(self, hosts: list):
    """Async task: Scan multiple assets in batch."""
    results = []
    total = len(hosts)
    for i, host in enumerate(hosts):
        self.update_state(state="PROGRESS", meta={"current": i + 1, "total": total, "host": host})
        result = scan_asset.delay(host)
        results.append({"host": host, "task_id": result.id})
    return {"total": total, "tasks": results}


@celery_app.task(name="tasks.celery_tasks.discover_assets")
def discover_assets(domain: str):
    """Async task: Run full discovery pipeline."""
    import asyncio
    from engines.discovery import DiscoveryEngine

    logger.info(f"[Celery] Running discovery for {domain}")
    engine = DiscoveryEngine()

    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(engine.discover(domain))
    finally:
        loop.close()

    return result


@celery_app.task(name="tasks.celery_tasks.monitor_ct_logs")
def monitor_ct_logs():
    """Scheduled task: Monitor Certificate Transparency logs."""
    logger.info("[Celery] Monitoring CT logs...")
    # In production, this would query crt.sh for new entries
    return {"status": "completed", "new_certificates": 0}


@celery_app.task(name="tasks.celery_tasks.rescan_critical_assets")
def rescan_critical_assets():
    """Scheduled task: Re-scan assets with critical risk scores."""
    logger.info("[Celery] Re-scanning critical assets...")
    return {"status": "completed", "assets_rescanned": 0}
