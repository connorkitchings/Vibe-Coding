from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from ..services import StateService, TelemetryService

# Setup templates (need to access same templates dir)
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(prefix="/components", tags=["components"])


@router.get("/blackboard")
async def blackboard(request: Request):
    service = StateService()
    blackboard_data = service.get_blackboard()
    # Sort messages by timestamp desc
    blackboard_data["messages"] = sorted(
        blackboard_data.get("messages", []),
        key=lambda x: x.get("timestamp", ""),
        reverse=True,
    )
    return templates.TemplateResponse(
        "components/blackboard.html",
        {"request": request, "blackboard": blackboard_data},
    )


@router.get("/metrics")
async def metrics(request: Request):
    service = TelemetryService()
    metrics_data = service.get_metrics_summary()
    return templates.TemplateResponse(
        "components/metrics.html", {"request": request, "metrics": metrics_data}
    )


@router.get("/sprints")
async def sprints(request: Request):
    service = TelemetryService()
    history = service.get_sprint_history()
    return templates.TemplateResponse(
        "components/sprints.html", {"request": request, "history": history}
    )
