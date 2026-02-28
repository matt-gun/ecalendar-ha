from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .db import init_db
from .models import Event, Chore, TodoList, TodoItem, Category, CalendarSync
from .api import events, chores, lists, categories, weather, sync

STATIC_DIR = Path("/usr/share/nginx/html")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass


app = FastAPI(
    title="eCalendar",
    description="Daily planner - events, chores, lists, weather",
    version="1.0.7",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(chores.router)
app.include_router(lists.router)
app.include_router(categories.router)
app.include_router(weather.router)
app.include_router(sync.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")
    file_path = STATIC_DIR / full_path
    if file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(STATIC_DIR / "index.html")
