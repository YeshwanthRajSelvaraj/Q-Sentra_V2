"""
Q-Sentra WebSocket Manager
Handles real-time push notifications to connected dashboard clients.
"""
import json
import asyncio
from typing import Dict, Set
from fastapi import WebSocket


class WebSocketManager:
    """Manages WebSocket connections and broadcasts real-time updates."""

    def __init__(self):
        self._connections: Dict[str, Set[WebSocket]] = {}
        self._all: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, channel: str = "general"):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self._all.add(websocket)
        if channel not in self._connections:
            self._connections[channel] = set()
        self._connections[channel].add(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from all channels."""
        self._all.discard(websocket)
        for channel in self._connections.values():
            channel.discard(websocket)

    async def broadcast(self, message: dict, channel: str = "general"):
        """Broadcast a JSON message to all clients on a channel."""
        targets = self._connections.get(channel, self._all)
        dead = set()
        for ws in targets:
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect(ws)

    async def broadcast_all(self, message: dict):
        """Broadcast to ALL connected clients regardless of channel."""
        dead = set()
        for ws in self._all:
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect(ws)

    async def send_scan_update(self, asset_id: str, status: str, data: dict = None):
        """Send a scan progress update."""
        await self.broadcast({
            "type": "scan_update",
            "asset_id": asset_id,
            "status": status,
            "data": data or {},
        })

    async def send_discovery_update(self, discovered: list):
        """Send a discovery result update."""
        await self.broadcast({
            "type": "discovery_update",
            "assets_found": len(discovered),
            "data": discovered,
        })

    @property
    def active_connections(self) -> int:
        return len(self._all)


# Global singleton
ws_manager = WebSocketManager()
