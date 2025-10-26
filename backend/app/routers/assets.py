from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import crud
from ..dependencies import SessionDep
from ..models import Asset
from ..schemas import AssetCreate, AssetRead

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=list[AssetRead])
def list_assets(session: SessionDep) -> list[Asset]:
    return list(crud.list_assets(session))


@router.post("", response_model=AssetRead, status_code=201)
def create_asset_endpoint(asset_in: AssetCreate, session: SessionDep) -> Asset:
    asset = Asset(**asset_in.model_dump())
    return crud.create_asset(session, asset)


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset_endpoint(asset_id: int, session: SessionDep) -> Asset:
    asset = crud.get_asset(session, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
