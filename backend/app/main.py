from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .routers import assets, commands, playlists, screens

app = FastAPI(title="Venue Screen Control", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(assets.router)
app.include_router(playlists.router)
app.include_router(screens.router)
app.include_router(commands.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Screen control backend is running"}


FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

control_dir = FRONTEND_DIR / "control"
player_dir = FRONTEND_DIR / "player"
if control_dir.exists():
    app.mount("/control", StaticFiles(directory=control_dir, html=True), name="control")
if player_dir.exists():
    app.mount("/player", StaticFiles(directory=player_dir, html=True), name="player")
