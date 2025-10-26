from __future__ import annotations

from typing import Iterable, Sequence

from sqlmodel import Session, select

from .models import Asset, Playlist, PlaylistItem, Screen
from .schemas import PlaylistAssignment, PlaylistCreate, PlaylistItemCreate, ScreenUpdate


# Screens

def list_screens(session: Session) -> Sequence[Screen]:
    return session.exec(select(Screen)).all()


def create_screen(session: Session, screen: Screen) -> Screen:
    session.add(screen)
    session.commit()
    session.refresh(screen)
    return screen


def get_screen(session: Session, screen_id: int) -> Screen | None:
    return session.get(Screen, screen_id)


def update_screen(session: Session, screen: Screen, data: ScreenUpdate) -> Screen:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(screen, key, value)
    session.add(screen)
    session.commit()
    session.refresh(screen)
    return screen


def assign_playlist(session: Session, screen: Screen, assignment: PlaylistAssignment) -> Screen:
    screen.assigned_playlist_id = assignment.playlist_id
    screen.fit_mode = assignment.fit_mode
    screen.crop_settings = assignment.crop_settings.model_dump() if assignment.crop_settings else None
    if assignment.playback_volume is not None:
        screen.playback_volume = assignment.playback_volume
    session.add(screen)
    session.commit()
    session.refresh(screen)
    return screen


# Assets

def create_asset(session: Session, asset: Asset) -> Asset:
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset


def list_assets(session: Session) -> Sequence[Asset]:
    return session.exec(select(Asset)).all()


def get_asset(session: Session, asset_id: int) -> Asset | None:
    return session.get(Asset, asset_id)


# Playlists

def create_playlist(session: Session, playlist_data: PlaylistCreate) -> Playlist:
    playlist = Playlist(
        name=playlist_data.name,
        description=playlist_data.description,
        playback_mode=playlist_data.playback_mode,
        default_duration_seconds=playlist_data.default_duration_seconds,
        metadata=playlist_data.metadata,
    )
    playlist.items = [
        PlaylistItem(
            asset_id=item.asset_id,
            order_index=item.order_index,
            display_duration_seconds=item.display_duration_seconds,
            crop_settings=item.crop_settings.model_dump() if item.crop_settings else None,
            fit_mode=item.fit_mode,
        )
        for item in sorted(playlist_data.items, key=lambda it: it.order_index)
    ]
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist


def get_playlist(session: Session, playlist_id: int) -> Playlist | None:
    return session.get(Playlist, playlist_id)


def list_playlists(session: Session) -> Sequence[Playlist]:
    return session.exec(select(Playlist)).unique().all()


def replace_playlist_items(session: Session, playlist: Playlist, items: Iterable[PlaylistItemCreate]) -> Playlist:
    playlist.items = [
        PlaylistItem(
            asset_id=item.asset_id,
            order_index=item.order_index,
            display_duration_seconds=item.display_duration_seconds,
            crop_settings=item.crop_settings.model_dump() if item.crop_settings else None,
            fit_mode=item.fit_mode,
        )
        for item in sorted(items, key=lambda it: it.order_index)
    ]
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist
