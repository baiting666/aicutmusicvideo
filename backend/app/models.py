from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class AssetType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    STREAM = "stream"


class PlaybackMode(str, Enum):
    SEQUENTIAL = "sequential"
    LOOP_LIST = "loop_list"
    LOOP_SINGLE = "loop_single"


class FitMode(str, Enum):
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"


class ScreenBase(SQLModel):
    name: str
    location: Optional[str] = None
    width: int
    height: int
    orientation: str = "landscape"
    brightness: Optional[int] = Field(default=None, ge=0, le=100)
    metadata: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})


class Screen(ScreenBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_playlist_id: Optional[int] = Field(default=None, foreign_key="playlist.id")
    crop_settings: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})
    fit_mode: FitMode = Field(default=FitMode.COVER)
    playback_volume: Optional[int] = Field(default=50, ge=0, le=100)

    assigned_playlist: "Playlist | None" = Relationship(back_populates="screens")


class AssetBase(SQLModel):
    name: str
    asset_type: AssetType
    source_uri: str
    duration_seconds: Optional[int] = Field(default=None, ge=1)
    width: Optional[int] = Field(default=None, ge=1)
    height: Optional[int] = Field(default=None, ge=1)
    metadata: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})


class Asset(AssetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    playlist_items: list["PlaylistItem"] = Relationship(back_populates="asset")


class PlaylistBase(SQLModel):
    name: str
    description: Optional[str] = None
    playback_mode: PlaybackMode = PlaybackMode.SEQUENTIAL
    default_duration_seconds: Optional[int] = Field(default=None, ge=1)
    metadata: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})


class Playlist(PlaylistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    items: list["PlaylistItem"] = Relationship(
        back_populates="playlist",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "joined"},
    )
    screens: list[Screen] = Relationship(back_populates="assigned_playlist")


class PlaylistItemBase(SQLModel):
    order_index: int = Field(ge=0)
    display_duration_seconds: Optional[int] = Field(default=None, ge=1)
    crop_settings: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})
    fit_mode: FitMode = Field(default=FitMode.CONTAIN)


class PlaylistItem(PlaylistItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id: int = Field(foreign_key="playlist.id")
    asset_id: int = Field(foreign_key="asset.id")

    playlist: Playlist = Relationship(back_populates="items")
    asset: Asset = Relationship(back_populates="playlist_items", sa_relationship_kwargs={"lazy": "joined"})
