"""WebSocket connection manager for real-time updates."""

import json
from typing import List
from fastapi import WebSocket


class WebSocketManager:
    """Manages WebSocket connections for real-time dashboard updates."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)

    async def send_scan_update(self, scan_id: str, status: str, data: dict = None):
        await self.broadcast({
            "type": "scan_update",
            "scanId": scan_id,
            "status": status,
            "data": data or {},
        })

    async def send_asset_update(self, asset_id: str, data: dict):
        await self.broadcast({
            "type": "asset_update",
            "assetId": asset_id,
            "data": data,
        })

    async def send_alert(self, severity: str, message: str, details: dict = None):
        await self.broadcast({
            "type": "alert",
            "severity": severity,
            "message": message,
            "details": details or {},
        })


ws_manager = WebSocketManager()
