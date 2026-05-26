from .api_model import APIModel
from .mixins import CachedAtMixin


class RuntimeBucket(APIModel):
    range_start_ms: float
    range_end_ms: float
    count: int


class FunctionRuntime(APIModel):
    function: str
    count: int
    success_count: int
    failure_count: int
    avg_runtime_ms: float
    p50_runtime_ms: float
    p95_runtime_ms: float
    p99_runtime_ms: float
    min_runtime_ms: float
    max_runtime_ms: float
    runtime_buckets: list[RuntimeBucket]


class ThroughputStats(APIModel):
    jobs_last_hour: int
    jobs_last_5min: int
    throughput_per_min: float


class FunctionStatsResponse(CachedAtMixin, APIModel):
    functions: list[FunctionRuntime]
    throughput: ThroughputStats
