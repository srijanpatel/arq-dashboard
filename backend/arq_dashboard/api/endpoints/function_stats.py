import math
from collections import defaultdict
from datetime import UTC, datetime, timedelta

from arq.jobs import JobStatus
from fastapi import APIRouter, Depends

from arq_dashboard.cache import async_ttl_cache
from arq_dashboard.core.settings import settings
from arq_dashboard.dependencies import get_queue_name
from arq_dashboard.queue import Queue
from arq_dashboard.schemas.function_stats import (
    FunctionRuntime,
    FunctionStatsResponse,
    RuntimeBucket,
    ThroughputStats,
)

router = APIRouter()


def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    k = (len(sorted_values) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_values[int(k)]
    return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)


def build_buckets(runtimes: list[float], num_buckets: int = 10) -> list[RuntimeBucket]:
    if not runtimes:
        return []

    min_rt = min(runtimes)
    max_rt = max(runtimes)

    if min_rt == max_rt:
        return [
            RuntimeBucket(
                range_start_ms=min_rt,
                range_end_ms=max_rt,
                count=len(runtimes),
            )
        ]

    step = (max_rt - min_rt) / num_buckets
    buckets: list[RuntimeBucket] = []

    for i in range(num_buckets):
        start = min_rt + i * step
        end = start + step
        if i < num_buckets - 1:
            count = sum(1 for r in runtimes if start <= r < end)
        else:
            count = sum(1 for r in runtimes if start <= r <= end)
        buckets.append(
            RuntimeBucket(
                range_start_ms=round(start, 1),
                range_end_ms=round(end, 1),
                count=count,
            )
        )

    return buckets


@async_ttl_cache(ttl=settings.cache_ttl, maxsize=settings.cache_max_size)
async def _get_function_stats(queue_name: str) -> FunctionStatsResponse:
    queue = Queue.from_name(queue_name)
    jobs = await queue.get_jobs(JobStatus.complete)

    grouped: dict[str, list] = defaultdict(list)
    for job in jobs:
        grouped[job.function].append(job)

    functions: list[FunctionRuntime] = []

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
            p50 = percentile(runtimes_ms, 50)
            p95 = percentile(runtimes_ms, 95)
            p99 = percentile(runtimes_ms, 99)
            min_rt = runtimes_ms[0]
            max_rt = runtimes_ms[-1]
        else:
            avg = p50 = p95 = p99 = min_rt = max_rt = 0.0

        functions.append(
            FunctionRuntime(
                function=func_name,
                count=len(func_jobs),
                success_count=success_count,
                failure_count=failure_count,
                avg_runtime_ms=round(avg, 1),
                p50_runtime_ms=round(p50, 1),
                p95_runtime_ms=round(p95, 1),
                p99_runtime_ms=round(p99, 1),
                min_runtime_ms=round(min_rt, 1),
                max_runtime_ms=round(max_rt, 1),
                runtime_buckets=build_buckets(runtimes_ms),
            )
        )

    # Compute throughput
    now = datetime.now(UTC)
    hour_ago = now - timedelta(hours=1)
    five_min_ago = now - timedelta(minutes=5)

    jobs_last_hour = sum(
        1 for job in jobs if job.finish_time and job.finish_time >= hour_ago
    )
    jobs_last_5min = sum(
        1 for job in jobs if job.finish_time and job.finish_time >= five_min_ago
    )
    throughput_per_min = round(jobs_last_hour / 60, 2) if jobs_last_hour else 0.0

    throughput = ThroughputStats(
        jobs_last_hour=jobs_last_hour,
        jobs_last_5min=jobs_last_5min,
        throughput_per_min=throughput_per_min,
    )

    return FunctionStatsResponse(functions=functions, throughput=throughput)


@router.get("/", response_model=FunctionStatsResponse)
async def get_function_stats(
    queue_name: str = Depends(get_queue_name),
) -> FunctionStatsResponse:
    return await _get_function_stats(queue_name)
