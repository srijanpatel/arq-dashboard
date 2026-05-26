from datetime import datetime

from arq.jobs import JobStatus
from fastapi import APIRouter, Depends, HTTPException, Query

from arq_dashboard import schemas
from arq_dashboard.cache import async_ttl_cache
from arq_dashboard.core.settings import settings
from arq_dashboard.dependencies import get_queue_name
from arq_dashboard.queue import Queue

router = APIRouter()


def filter_by_start_time(job: schemas.JobInfo, start_time: datetime | None):
    if start_time is None:
        return True
    if job.start_time is None:
        return True
    return job.start_time >= start_time


def filter_by_finish_time(job: schemas.JobInfo, finish_time: datetime | None):
    if finish_time is None:
        return True
    if job.finish_time is None:
        return True
    return job.finish_time <= finish_time


def filter_by_function(job: schemas.JobInfo, func: str | None):
    if func is None:
        return True
    return job.function == func


def filter_by_queue_name(
    job: schemas.JobInfo, queue_name: str, *, allow_none_queue_name: bool = True
):
    if job.queue_name is None and allow_none_queue_name:
        return True
    return job.queue_name == queue_name


def filter_by_success(job: schemas.JobInfo, success: bool | None):
    if success is None:
        return True
    return job.success is success


def apply_filters(
    jobs: list[schemas.JobInfo],
    *,
    queue_name: str,
    allow_none_queue_name: bool = True,
    success: bool | None = None,
    start_time: datetime | None = None,
    finish_time: datetime | None = None,
    function_name: str | None = None,
) -> list[schemas.JobInfo]:
    return [
        job
        for job in jobs
        if filter_by_queue_name(
            job, queue_name, allow_none_queue_name=allow_none_queue_name
        )
        and filter_by_success(job, success)
        and filter_by_function(job, function_name)
        and filter_by_start_time(job, start_time)
        and filter_by_finish_time(job, finish_time)
    ]


@async_ttl_cache(ttl=settings.cache_ttl, maxsize=settings.cache_max_size)
async def _get_jobs(
    queue_name: str,
    *,
    status: JobStatus | None = None,
) -> list[schemas.JobInfo]:
    queue = Queue.from_name(queue_name)
    return await queue.get_jobs(status)


@router.get("/", response_model=schemas.JobsWithPagination)
async def get_jobs(
    page: int = 1,
    success: bool | None = None,
    status: JobStatus | None = None,
    start_time: datetime | None = Query(None, alias="startTime"),
    finish_time: datetime | None = Query(None, alias="finishTime"),
    function_name: str | None = Query(None, alias="functionName"),
    *,
    queue_name: str = Depends(get_queue_name),
) -> schemas.JobsWithPagination:
    jobs = await _get_jobs(queue_name, status=status)

    filtered_jobs = apply_filters(
        jobs,
        queue_name=queue_name,
        success=success,
        start_time=start_time,
        finish_time=finish_time,
        function_name=function_name,
    )

    limit = 100
    offset = (page - 1) * limit
    total = len(jobs)

    return schemas.JobsWithPagination(
        jobs=filtered_jobs[offset : offset + limit],
        total=total,
        current_page=page,
        page_size=limit,
    )


@async_ttl_cache(ttl=settings.cache_ttl, maxsize=settings.cache_max_size)
async def _get_job_by_id(id: str, *, queue_name: str) -> schemas.CachedJobInfo:
    queue = Queue.from_name(queue_name)
    job_info = await queue.get_job_by_id(id)
    return schemas.CachedJobInfo.model_validate(job_info.model_dump())


@router.get("/{id}", response_model=schemas.CachedJobInfo)
async def get_job_by_id(
    id: str, *, queue_name: str = Depends(get_queue_name)
) -> schemas.CachedJobInfo:
    job = await _get_job_by_id(id, queue_name=queue_name)
    if job.status == "not_found":
        raise HTTPException(status_code=404, detail=f"Job:{id} not found")
    return job
