from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import crud
from ..dependencies import SessionDep
from ..schemas import CommandPayload
from ..websocket_manager import manager

router = APIRouter(prefix="/commands", tags=["commands"])


@router.post("/screens/{screen_id}")
async def send_command_to_screen(
    screen_id: int, command: CommandPayload, session: SessionDep
) -> dict[str, str]:
    screen = crud.get_screen(session, screen_id)
    if not screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    payload = {"event": command.command_type, "payload": command.payload}
    await manager.send_to_screen(screen_id, payload)
    return {"status": "sent"}


@router.post("/broadcast")
async def broadcast_command(command: CommandPayload) -> dict[str, str]:
    payload = {"event": command.command_type, "payload": command.payload}
    await manager.broadcast(payload)
    return {"status": "sent"}
