from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .api.api import api_router
from .core.settings import settings
from .errors import ArqDashboardError, InvalidQueueNameError

FRONTEND_DIR = Path(__file__).parent / "frontend"


def handle_arq_dashboard_error(_request: Request, error: ArqDashboardError):
    if isinstance(error, InvalidQueueNameError):
        return JSONResponse(status_code=400, content={"detail": str(error)})
    return JSONResponse(status_code=500, content={"detail": str(error)})


def create_app() -> FastAPI:
    logger.add(
        settings.log_file,
        level=settings.log_level,
        backtrace=settings.log_backtrace,
    )

    app = FastAPI(debug=settings.debug, title=settings.project_name)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.include_router(api_router, prefix="/api")
    app.add_exception_handler(ArqDashboardError, handle_arq_dashboard_error)

    if FRONTEND_DIR.exists():
        app.mount(
            "/",
            StaticFiles(html=True, directory=FRONTEND_DIR),
            name="static",
        )

    return app
