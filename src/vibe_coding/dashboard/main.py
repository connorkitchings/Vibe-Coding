from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .services import StateService, TelemetryService

# Create FastAPI app
app = FastAPI(
    title="Vibe Dashboard",
    description="Control center for MADE orchestrator",
    version="1.0.0",
)

# Get project root and setup paths
BASE_DIR = Path(__file__).resolve().parent
# src/vibe_coding/dashboard -> src/vibe_coding -> src -> root
PROJECT_ROOT = BASE_DIR.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


from .services import StateService
from .routers import components

# Include routers
app.include_router(components.router)


@app.get("/")
async def index(request: Request):
    state_service = StateService()
    sprint_status = state_service.get_sprint_status()
    active_agent = state_service.get_active_agent()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "sprint": sprint_status, "active_agent": active_agent},
    )


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
