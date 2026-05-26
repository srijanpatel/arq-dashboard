from fastapi import APIRouter

from .endpoints import function_stats, functions, jobs, queues, stats

api_router = APIRouter()

api_router.include_router(functions.router, prefix="/functions")
api_router.include_router(function_stats.router, prefix="/stats/functions")
api_router.include_router(jobs.router, prefix="/jobs")
api_router.include_router(queues.router, prefix="/queues")
api_router.include_router(stats.router, prefix="/stats")
