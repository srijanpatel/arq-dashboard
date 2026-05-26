from datetime import datetime
from typing import Any

from arq.jobs import JobDef as ArqJobDef
from arq.jobs import JobResult, JobStatus

from .api_model import APIModel
from .mixins import CachedAtMixin, PaginationMixin


class JobDef(APIModel):
    function: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    job_try: int | None
    enqueue_time: datetime | None = None
    score: int | None = None


class JobInfo(JobDef):
    job_id: str
    success: bool = False
    queue_name: str | None = None
    result: Any | None = None
    start_time: datetime | None = None
    finish_time: datetime | None = None
    status: JobStatus = JobStatus.queued

    @classmethod
    def from_base(
        cls, base_info: ArqJobDef | JobDef | JobResult, job_id: str
    ) -> "JobInfo":
        obj = cls(
            job_id=job_id,
            function=base_info.function,
            args=base_info.args,
            kwargs=base_info.kwargs,
            job_try=base_info.job_try,
            enqueue_time=base_info.enqueue_time,
            score=base_info.score,
        )

        if isinstance(base_info, JobResult):
            obj.success = base_info.success
            obj.result = base_info.result
            obj.start_time = base_info.start_time
            obj.finish_time = base_info.finish_time
            obj.queue_name = base_info.queue_name

        return obj


class CachedJobInfo(CachedAtMixin, JobInfo, APIModel):
    pass


class JobsWithPagination(CachedAtMixin, PaginationMixin, APIModel):
    jobs: list[JobInfo]
