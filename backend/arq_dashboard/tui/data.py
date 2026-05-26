"""Data fetching for the TUI — talks directly to Redis, no HTTP."""

import math
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from arq.constants import default_queue_name
from arq.jobs import JobStatus

from arq_dashboard.core.settings import settings
from arq_dashboard.queue import Queue


@dataclass
class FunctionPerf:
    function: str
    count: int
    success_count: int
    avg_runtime_ms: float
    p50_runtime_ms: float
    p95_runtime_ms: float
    p99_runtime_ms: float


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


async def fetch_all_data() -> DashboardData:
    queue_name = default_queue_name
    queue = Queue(
        name=queue_name,
        redis_settings=settings.redis_settings,
    )

    data = DashboardData(
        cached_at=datetime.now(UTC).strftime("%H:%M:%S"),
    )

    # Get all jobs for stats
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
                avg_runtime_ms=round(avg, 1),
                p50_runtime_ms=round(p50, 1),
                p95_runtime_ms=round(p95, 1),
                p99_runtime_ms=round(p99, 1),
            )
        )

    return data
