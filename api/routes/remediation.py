"""Remediation Orchestrator routes."""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

TASKS = [
    {"taskId": "REM-001", "assetId": "web01.pnb.co.in", "title": "Upgrade web01 to TLS 1.3 with ML-KEM", "description": "Replace RSA key exchange with ML-KEM-768, upgrade TLS to 1.3", "priority": "critical", "status": "pending", "phase": 1, "effortHours": 40, "dueDate": "2026-06-30"},
    {"taskId": "REM-002", "assetId": "netbanking.pnb.co.in", "title": "Migrate net banking to quantum-safe TLS", "description": "Full PQC migration: ML-KEM-768 KEX, ML-DSA-65 signatures", "priority": "critical", "status": "in_progress", "phase": 1, "effortHours": 80, "dueDate": "2026-07-31"},
    {"taskId": "REM-003", "assetId": "api.pnb.co.in", "title": "API gateway PQC upgrade", "description": "Enable X25519+Kyber768 hybrid mode", "priority": "high", "status": "pending", "phase": 2, "effortHours": 60, "dueDate": "2026-09-30"},
    {"taskId": "REM-004", "assetId": "vpn.pnb.co.in", "title": "VPN quantum-safe migration", "description": "Migrate VPN from RSA to ML-KEM", "priority": "high", "status": "pending", "phase": 2, "effortHours": 50, "dueDate": "2026-10-31"},
    {"taskId": "REM-005", "assetId": "upi.pnb.co.in", "title": "UPI payment gateway PQC hardening", "description": "Implement hybrid X25519+Kyber768", "priority": "critical", "status": "pending", "phase": 1, "effortHours": 100, "dueDate": "2026-08-31"},
    {"taskId": "REM-006", "assetId": "mail.pnb.co.in", "title": "Email server TLS upgrade", "description": "Upgrade mail server TLS with PQC algorithms", "priority": "medium", "status": "pending", "phase": 3, "effortHours": 30, "dueDate": "2026-12-31"},
    {"taskId": "REM-007", "assetId": "cdn.pnb.co.in", "title": "CDN edge PQC configuration", "description": "Configure Cloudflare PQC support", "priority": "medium", "status": "pending", "phase": 3, "effortHours": 20, "dueDate": "2027-01-31"},
    {"taskId": "REM-008", "assetId": "mobile.pnb.co.in", "title": "Mobile API PQC integration", "description": "Update mobile SDK for PQC support", "priority": "high", "status": "in_progress", "phase": 2, "effortHours": 70, "dueDate": "2026-09-30"},
    {"taskId": "REM-009", "assetId": "imps.pnb.co.in", "title": "IMPS gateway optimization", "description": "Optimize existing Kyber768 implementation", "priority": "low", "status": "completed", "phase": 1, "effortHours": 25, "dueDate": "2026-04-30"},
]


class UpdateTaskRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignedTo: Optional[str] = None


@router.get("")
async def list_tasks(status: Optional[str] = None):
    tasks = TASKS if not status else [t for t in TASKS if t["status"] == status]
    return {"data": tasks, "summary": {"pending": len([t for t in TASKS if t["status"] == "pending"]), "inProgress": len([t for t in TASKS if t["status"] == "in_progress"]), "completed": len([t for t in TASKS if t["status"] == "completed"])}}


@router.get("/roadmap")
async def get_migration_roadmap():
    return {"phases": [
        {"phase": 1, "name": "Critical Assets", "timeline": "Apr-Jul 2026", "tasks": [t for t in TASKS if t["phase"] == 1], "status": "in_progress"},
        {"phase": 2, "name": "High Priority Assets", "timeline": "Aug-Oct 2026", "tasks": [t for t in TASKS if t["phase"] == 2], "status": "planned"},
        {"phase": 3, "name": "Remaining Assets", "timeline": "Nov 2026-Jan 2027", "tasks": [t for t in TASKS if t["phase"] == 3], "status": "planned"},
    ], "totalMonths": 9, "completionTarget": "2027-01-31"}


@router.get("/{task_id}")
async def get_task(task_id: str):
    task = next((t for t in TASKS if t["taskId"] == task_id), None)
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/{task_id}/playbook")
async def get_playbook(task_id: str):
    return {"taskId": task_id, "playbook": {
        "name": f"PQC Migration - {task_id}",
        "steps": [
            {"order": 1, "action": "Backup current TLS configuration", "command": "cp /etc/nginx/ssl/ /backup/ssl-$(date +%Y%m%d)/"},
            {"order": 2, "action": "Install PQC-enabled OpenSSL", "command": "apt install openssl-pqc"},
            {"order": 3, "action": "Generate ML-KEM-768 keypair", "command": "openssl genpkey -algorithm mlkem768 -out server-mlkem.key"},
            {"order": 4, "action": "Update TLS configuration", "command": "sed -i 's/ssl_protocols.*/ssl_protocols TLSv1.3;/' /etc/nginx/nginx.conf"},
            {"order": 5, "action": "Restart service and validate", "command": "systemctl restart nginx && openssl s_client -connect localhost:443"},
        ],
        "ansibleYaml": "---\n- name: PQC Migration Playbook\n  hosts: target_servers\n  become: yes\n  tasks:\n    - name: Backup TLS config\n      copy:\n        src: /etc/nginx/ssl/\n        dest: /backup/ssl-{{ ansible_date_time.date }}/\n        remote_src: yes\n    - name: Install PQC OpenSSL\n      apt:\n        name: openssl-pqc\n        state: present\n    - name: Generate ML-KEM keypair\n      command: openssl genpkey -algorithm mlkem768 -out /etc/nginx/ssl/server-mlkem.key\n    - name: Update nginx config\n      lineinfile:\n        path: /etc/nginx/nginx.conf\n        regexp: 'ssl_protocols'\n        line: '    ssl_protocols TLSv1.3;'\n    - name: Restart nginx\n      service:\n        name: nginx\n        state: restarted\n",
    }}


@router.patch("/{task_id}")
async def update_task(task_id: str, request: UpdateTaskRequest):
    task = next((t for t in TASKS if t["taskId"] == task_id), None)
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    if request.status: task["status"] = request.status
    if request.priority: task["priority"] = request.priority
    return task
