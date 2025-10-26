from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlmodel import Session

from .. import crud
from ..database import get_session
from ..dependencies import SessionDep
from ..models import Screen
from ..schemas import PlaylistAssignment, ScreenCreate, ScreenRead, ScreenUpdate
from ..websocket_manager import manager

router = APIRouter(prefix="/screens", tags=["screens"])


@router.get("", response_model=list[ScreenRead])
def get_screens(session: SessionDep) -> list[Screen]:
    return list(crud.list_screens(session))


@router.post("", response_model=ScreenRead, status_code=201)
def create_screen_endpoint(screen_in: ScreenCreate, session: SessionDep) -> Screen:
    screen = Screen(**screen_in.model_dump())
    return crud.create_screen(session, screen)


@router.get("/{screen_id}", response_model=ScreenRead)
def get_screen_endpoint(screen_id: int, session: SessionDep) -> Screen:
    screen = crud.get_screen(session, screen_id)
    if not screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    return screen


@router.patch("/{screen_id}", response_model=ScreenRead)
def update_screen_endpoint(screen_id: int, screen_update: ScreenUpdate, session: SessionDep) -> Screen:
    screen = crud.get_screen(session, screen_id)
    if not screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    return crud.update_screen(session, screen, screen_update)


@router.post("/{screen_id}/playlist", response_model=ScreenRead)
def assign_playlist_endpoint(
    screen_id: int, assignment: PlaylistAssignment, session: SessionDep
) -> Screen:
    screen = crud.get_screen(session, screen_id)
    if not screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    playlist = crud.get_playlist(session, assignment.playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    updated = crud.assign_playlist(session, screen, assignment)
    payload = {
        "event": "playlist_assigned",
        "screen_id": screen_id,
        "playlist_id": assignment.playlist_id,
        "fit_mode": assignment.fit_mode,
        "crop_settings": assignment.crop_settings.model_dump() if assignment.crop_settings else None,
        "playback_volume": assignment.playback_volume,
    }
    asyncio.create_task(manager.send_to_screen(screen_id, payload))
    return updated


@router.websocket("/ws/{screen_id}")
async def screen_ws(websocket: WebSocket, screen_id: int, session: Session = Depends(get_session)) -> None:
    screen = crud.get_screen(session, screen_id)
    if not screen:
        await websocket.close(code=4004)
        return
    await manager.connect(screen_id, websocket)
    try:
        await websocket.send_json(
            {
                "event": "connected",
                "screen_id": screen_id,
                "assigned_playlist_id": screen.assigned_playlist_id,
                "fit_mode": str(screen.fit_mode),
                "crop_settings": screen.crop_settings,
                "playback_volume": screen.playback_volume,
            }
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(screen_id, websocket)

