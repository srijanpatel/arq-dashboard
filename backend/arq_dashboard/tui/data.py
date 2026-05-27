"""Data fetching for the TUI — talks directly to Redis, no HTTP."""

import math
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from arq.constants import default_queue_name
from arq.jobs import JobStatus

from arq_dashboard.core.settings import settings
from arq_dashboard.queue import Queue


@dataclass
class FunctionPerf:
    function: str
    count: int
    success_count: int
    failure_count: int
    avg_runtime_ms: float
    p50_runtime_ms: float
    p95_runtime_ms: float
    p99_runtime_ms: float


@dataclass
class JobRow:
    job_id: str
    function: str
    status: str
    success: bool
    queue_name: str
    enqueue_time: str
    runtime_ms: float | None
    # Detail fields (used by JobDetailScreen)
    enqueue_time_dt: datetime | None = None
    start_time_dt: datetime | None = None
    finish_time_dt: datetime | None = None
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    job_try: int | None = None


@dataclass
class DashboardData:
    queued_jobs: int = 0
    in_progress_jobs: int = 0
    deferred_jobs: int = 0
    complete_jobs: int = 0
    not_found_jobs: int = 0
    throughput_per_min: float = 0.0
    jobs_last_5min: int = 0
    jobs_last_hour: int = 0
    functions: list[FunctionPerf] = field(default_factory=list)
    jobs: list[JobRow] = field(default_factory=list)
    cached_at: str = ""


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


def _fmt_time(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return dt.strftime("%H:%M:%S")


async def fetch_all_data() -> DashboardData:
    queue_name = default_queue_name
    queue = Queue(
        name=queue_name,
        redis_settings=settings.redis_settings,
    )

    data = DashboardData(
        cached_at=datetime.now(UTC).strftime("%H:%M:%S"),
    )

    all_jobs = await queue.get_jobs()
    status_counts: dict[JobStatus, int] = {
        JobStatus.queued: 0,
        JobStatus.in_progress: 0,
        JobStatus.deferred: 0,
        JobStatus.complete: 0,
        JobStatus.not_found: 0,
    }
    for job in all_jobs:
        status_counts[job.status] = status_counts.get(job.status, 0) + 1

    data.queued_jobs = status_counts[JobStatus.queued]
    data.in_progress_jobs = status_counts[JobStatus.in_progress]
    data.deferred_jobs = status_counts[JobStatus.deferred]
    data.complete_jobs = status_counts[JobStatus.complete]
    data.not_found_jobs = status_counts[JobStatus.not_found]

    # Build job rows
    for job in all_jobs[:200]:
        runtime_ms = None
        if job.start_time and job.finish_time:
            runtime_ms = (job.finish_time - job.start_time).total_seconds() * 1000

        data.jobs.append(
            JobRow(
                job_id=job.job_id,
                function=job.function,
                status=str(job.status.value)
                if hasattr(job.status, "value")
                else str(job.status),
                success=job.success,
                queue_name=job.queue_name or "—",
                enqueue_time=_fmt_time(job.enqueue_time),
                runtime_ms=runtime_ms,
                enqueue_time_dt=job.enqueue_time,
                start_time_dt=job.start_time,
                finish_time_dt=job.finish_time,
                args=job.args,
                kwargs=job.kwargs,
                result=job.result,
                job_try=job.job_try,
            )
        )

    # Compute function stats from completed jobs
    completed = [j for j in all_jobs if j.status == JobStatus.complete]

    now = datetime.now(UTC)
    hour_ago = now - timedelta(hours=1)
    five_min_ago = now - timedelta(minutes=5)

    data.jobs_last_hour = sum(
        1 for j in completed if j.finish_time and j.finish_time >= hour_ago
    )
    data.jobs_last_5min = sum(
        1 for j in completed if j.finish_time and j.finish_time >= five_min_ago
    )
    data.throughput_per_min = (
        round(data.jobs_last_hour / 60, 2) if data.jobs_last_hour else 0.0
    )

    grouped: dict[str, list] = defaultdict(list)
    for job in completed:
        grouped[job.function].append(job)

    for func_name, func_jobs in sorted(grouped.items()):
        success_count = sum(1 for j in func_jobs if j.success)
        failure_count = len(func_jobs) - success_count

        runtimes_ms: list[float] = []
        for j in func_jobs:
            if j.start_time and j.finish_time:
                delta = (j.finish_time - j.start_time).total_seconds() * 1000
                runtimes_ms.append(delta)

        runtimes_ms.sort()
        if runtimes_ms:
            avg = sum(runtimes_ms) / len(runtimes_ms)
            p50 = _percentile(runtimes_ms, 50)
            p95 = _percentile(runtimes_ms, 95)
            p99 = _percentile(runtimes_ms, 99)
        else:
            avg = p50 = p95 = p99 = 0.0

        data.functions.append(
            FunctionPerf(
                function=func_name,
                count=len(func_jobs),
                success_count=success_count,
                failure_count=failure_count,
                avg_runtime_ms=round(avg, 1),
                p50_runtime_ms=round(p50, 1),
                p95_runtime_ms=round(p95, 1),
                p99_runtime_ms=round(p99, 1),
            )
        )

    return data


_MOCK_NOW = datetime(2026, 5, 26, 19, 42, 15, tzinfo=UTC)


def _mock_dt(ms_ago: int) -> datetime:
    return _MOCK_NOW - timedelta(milliseconds=ms_ago)


def mock_data() -> DashboardData:
    """Return realistic mock data for screenshots."""
    return DashboardData(
        queued_jobs=12,
        in_progress_jobs=7,
        deferred_jobs=3,
        complete_jobs=4821,
        not_found_jobs=0,
        throughput_per_min=14.12,
        jobs_last_5min=73,
        jobs_last_hour=847,
        cached_at="19:42:15",
        functions=[
            FunctionPerf(
                "send_notification", 2134, 2098, 36, 245.3, 180.0, 620.5, 1250.0
            ),
            FunctionPerf(
                "process_payment", 1456, 1432, 24, 1823.7, 1540.0, 3800.0, 5200.0
            ),
            FunctionPerf(
                "generate_report", 892, 871, 21, 12450.0, 10200.0, 24500.0, 38000.0
            ),
            FunctionPerf(
                "sync_inventory", 339, 339, 0, 4560.0, 3800.0, 8900.0, 12000.0
            ),
        ],
        jobs=[
            JobRow(
                job_id="e7d3e8f5bb064035ba71d6cfda0167d4",
                function="send_notification",
                status="complete",
                success=True,
                queue_name="arq:queue",
                enqueue_time="19:41:52",
                runtime_ms=210.5,
                enqueue_time_dt=_mock_dt(23800),
                start_time_dt=_mock_dt(23420),
                finish_time_dt=_mock_dt(23210),
                args=("user_4012", "order.shipped"),
                kwargs={"channel": "email", "priority": "normal"},
                result={"sent": True, "message_id": "msg_8a3f"},
                job_try=1,
            ),
            JobRow(
                job_id="a1604834e6df46f58c9cf1158baedfd9",
                function="process_payment",
                status="complete",
                success=True,
                queue_name="arq:queue",
                enqueue_time="19:41:44",
                runtime_ms=1823.0,
                enqueue_time_dt=_mock_dt(31200),
                start_time_dt=_mock_dt(30400),
                finish_time_dt=_mock_dt(28577),
                args=("usr_1042", "ord_88291"),
                kwargs={"currency": "USD", "amount": 49.99, "retry": False},
                result={"transactionId": "txn_9f8a7b6c", "status": "settled"},
                job_try=1,
            ),
            JobRow(
                "9011598986d0",
                "generate_report",
                "in_progress",
                False,
                "arq:queue",
                "19:41:38",
                None,
            ),
            JobRow(
                "ad8458b6dae9",
                "send_notification",
                "complete",
                True,
                "arq:queue",
                "19:41:30",
                180.2,
            ),
            JobRow(
                "1d8b3ce0ab89",
                "sync_inventory",
                "complete",
                True,
                "arq:queue",
                "19:41:22",
                4320.0,
            ),
            JobRow(
                "f3a2b1c0d9e8",
                "process_payment",
                "complete",
                False,
                "arq:queue",
                "19:41:15",
                5100.0,
            ),
            JobRow(
                "b5c4d3e2f1a0",
                "send_notification",
                "complete",
                True,
                "arq:queue",
                "19:41:08",
                195.0,
            ),
            JobRow(
                "c6d5e4f3a2b1",
                "generate_report",
                "complete",
                True,
                "arq:queue",
                "19:41:00",
                15200.0,
            ),
            JobRow(
                "d7e6f5a4b3c2",
                "send_notification",
                "queued",
                False,
                "arq:queue",
                "19:40:52",
                None,
            ),
            JobRow(
                "e8f7a6b5c4d3",
                "sync_inventory",
                "complete",
                True,
                "arq:queue",
                "19:40:45",
                3800.0,
            ),
            JobRow(
                "f9a8b7c6d5e4",
                "process_payment",
                "complete",
                True,
                "arq:queue",
                "19:40:38",
                1450.0,
            ),
            JobRow(
                "a0b9c8d7e6f5",
                "send_notification",
                "complete",
                True,
                "arq:queue",
                "19:40:30",
                230.0,
            ),
            JobRow(
                "b1c0d9e8f7a6",
                "generate_report",
                "deferred",
                False,
                "arq:queue",
                "19:40:22",
                None,
            ),
            JobRow(
                "c2d1e0f9a8b7",
                "send_notification",
                "complete",
                True,
                "arq:queue",
                "19:40:15",
                165.0,
            ),
            JobRow(
                "d3e2f1a0b9c8",
                "process_payment",
                "in_progress",
                False,
                "arq:queue",
                "19:40:08",
                None,
            ),
        ],
    )
