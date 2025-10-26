from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, DefaultDict

from fastapi import WebSocket


class ScreenConnectionManager:
    def __init__(self) -> None:
        self._connections: DefaultDict[int, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, screen_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections[screen_id].add(websocket)

    async def disconnect(self, screen_id: int, websocket: WebSocket) -> None:
        async with self._lock:
            connections = self._connections.get(screen_id)
            if connections and websocket in connections:
                connections.remove(websocket)
            if connections and not connections:
                self._connections.pop(screen_id, None)

    async def send_to_screen(self, screen_id: int, message: dict[str, Any]) -> None:
        async with self._lock:
            connections = list(self._connections.get(screen_id, set()))
        for connection in connections:
            await connection.send_json(message)

    async def broadcast(self, message: dict[str, Any]) -> None:
        async with self._lock:
            all_connections = [conn for conns in self._connections.values() for conn in conns]
        for connection in all_connections:
            await connection.send_json(message)


manager = ScreenConnectionManager()
