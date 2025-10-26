from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import crud
from ..dependencies import SessionDep
from ..models import Playlist
from ..schemas import PlaylistCreate, PlaylistItemCreate, PlaylistRead

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("", response_model=list[PlaylistRead])
def list_playlists(session: SessionDep) -> list[Playlist]:
    return list(crud.list_playlists(session))


@router.post("", response_model=PlaylistRead, status_code=201)
def create_playlist_endpoint(playlist_in: PlaylistCreate, session: SessionDep) -> Playlist:
    playlist = crud.create_playlist(session, playlist_in)
    return playlist


@router.get("/{playlist_id}", response_model=PlaylistRead)
def get_playlist_endpoint(playlist_id: int, session: SessionDep) -> Playlist:
    playlist = crud.get_playlist(session, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.put("/{playlist_id}/items", response_model=PlaylistRead)
def replace_items(
    playlist_id: int, items: list[PlaylistItemCreate], session: SessionDep
) -> Playlist:
    playlist = crud.get_playlist(session, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    updated = crud.replace_playlist_items(session, playlist, items)
    return updated
