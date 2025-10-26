from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from .models import AssetType, FitMode, PlaybackMode


class CropSettings(BaseModel):
    x: int = Field(0, ge=0)
    y: int = Field(0, ge=0)
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    anchor: str = Field("center", description="Anchor point for scaling (center, top-left, etc.)")


class ScreenBase(BaseModel):
    name: str
    location: Optional[str] = None
    width: int
    height: int
    orientation: str = "landscape"
    brightness: Optional[int] = Field(default=None, ge=0, le=100)
    metadata: dict | None = None


class ScreenCreate(ScreenBase):
    pass


class ScreenUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    orientation: Optional[str] = None
    brightness: Optional[int] = Field(default=None, ge=0, le=100)
    metadata: dict | None = None
    playback_volume: Optional[int] = Field(default=None, ge=0, le=100)


class ScreenRead(ScreenBase):
    id: int
    created_at: datetime
    assigned_playlist_id: Optional[int]
    crop_settings: Optional[CropSettings]
    fit_mode: FitMode
    playback_volume: Optional[int]

    class Config:
        from_attributes = True


class AssetBase(BaseModel):
    name: str
    asset_type: AssetType
    source_uri: HttpUrl | str
    duration_seconds: Optional[int] = Field(default=None, ge=1)
    width: Optional[int] = Field(default=None, ge=1)
    height: Optional[int] = Field(default=None, ge=1)
    metadata: dict | None = None


class AssetCreate(AssetBase):
    pass


class AssetRead(AssetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PlaylistItemBase(BaseModel):
    asset_id: int
    order_index: int = Field(ge=0)
    display_duration_seconds: Optional[int] = Field(default=None, ge=1)
    crop_settings: Optional[CropSettings] = None
    fit_mode: FitMode = FitMode.CONTAIN


class PlaylistItemCreate(PlaylistItemBase):
    pass


class PlaylistItemRead(PlaylistItemBase):
    id: int
    asset: AssetRead

    class Config:
        from_attributes = True


class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    playback_mode: PlaybackMode = PlaybackMode.SEQUENTIAL
    default_duration_seconds: Optional[int] = Field(default=None, ge=1)
    metadata: dict | None = None


class PlaylistCreate(PlaylistBase):
    items: list[PlaylistItemCreate] = []


class PlaylistRead(PlaylistBase):
    id: int
    created_at: datetime
    items: list[PlaylistItemRead]

    class Config:
        from_attributes = True


class PlaylistAssignment(BaseModel):
    playlist_id: int
    fit_mode: FitMode = FitMode.COVER
    crop_settings: Optional[CropSettings] = None
    playback_volume: Optional[int] = Field(default=None, ge=0, le=100)


class CommandPayload(BaseModel):
    command_type: str
    payload: dict = {}
