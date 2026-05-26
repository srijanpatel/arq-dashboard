import functools
from dataclasses import dataclass
from datetime import datetime

import aiometer
from arq import ArqRedis
from arq.connections import RedisSettings
from arq.constants import result_key_prefix
from arq.jobs import DeserializationError, JobDef, JobStatus
from arq.jobs import Job as ArqJob

from arq_dashboard import schemas
from arq_dashboard.core.settings import settings

from .dependencies import get_redis
from .errors import InvalidQueueNameError


async def scan(redis: ArqRedis, match: str) -> list[bytes]:
    result: list[bytes] = []
    cur, keys = await redis.scan(cursor=0, match=match)
    result.extend(keys)
    while cur != 0:
        cur, keys = await redis.scan(cursor=cur, match=match)
        result.extend(keys)
    return result


async def get_result_job_ids(redis: ArqRedis) -> set[str]:
    result_keys = await scan(redis, f"{result_key_prefix}*")
    return {key[len(result_key_prefix) :] for key in result_keys}


async def get_job_ids(redis: ArqRedis, queue_name: str) -> set[str]:
    job_ids = set(await redis.zrangebyscore(queue_name, "-inf", "inf"))
    job_ids |= await get_result_job_ids(redis)
    return {job_id.decode() for job_id in job_ids}


@dataclass
class Queue:
    name: str
    redis_settings: RedisSettings

    @classmethod
    def from_name(cls, name: str) -> "Queue":
        redis_settings = settings.arq_queues.get(name)
        if redis_settings is None:
            raise InvalidQueueNameError(f"Queue:{name} is not defined")
        return cls(name=name, redis_settings=redis_settings)

    async def get_jobs(
        self, status: JobStatus | None = None
    ) -> list[schemas.JobInfo]:
        async with get_redis(self.redis_settings) as redis:
            job_ids = await get_job_ids(redis, self.name)

            if status:
                job_ids_list = list(job_ids)
                if not job_ids_list:
                    return []

                filtered_job_ids = set(
                    await aiometer.run_all(
                        [
                            functools.partial(
                                self._filter_job_by_status, redis, job_id, status
                            )
                            for job_id in job_ids_list
                        ],
                        max_at_once=settings.max_at_once,
                        max_per_second=settings.max_per_seconds,
                    )
                )
                filtered_job_ids.discard(None)
                job_ids = filtered_job_ids

            if not job_ids:
                return []

            jobs: list[schemas.JobInfo] = await aiometer.run_all(
                [
                    functools.partial(self.get_job_by_id, job_id, redis)
                    for job_id in job_ids
                ],
                max_at_once=settings.max_at_once,
                max_per_second=settings.max_per_seconds,
            )

        dummy_enqueue_time = datetime.min
        return sorted(
            jobs,
            key=lambda x: (x.enqueue_time or dummy_enqueue_time).isoformat(),
            reverse=True,
        )

    async def get_stats(self) -> schemas.QueueStats:
        async with get_redis(self.redis_settings) as redis:
            job_ids = await get_job_ids(redis, self.name)

            statuses: list[JobStatus] = []
            if job_ids:
                statuses = await aiometer.run_all(
                    [
                        functools.partial(self._get_job_status, redis, job_id)
                        for job_id in job_ids
                    ],
                    max_at_once=settings.max_at_once,
                    max_per_second=settings.max_per_seconds,
                )

        job_counts: dict[JobStatus, int] = {
            JobStatus.queued: 0,
            JobStatus.in_progress: 0,
            JobStatus.deferred: 0,
            JobStatus.complete: 0,
            JobStatus.not_found: 0,
        }
        for s in statuses:
            job_counts[s] += 1

        return schemas.QueueStats(
            name=self.name,
            host=str(self.redis_settings.host),
            port=self.redis_settings.port,
            database=self.redis_settings.database,
            queued_jobs=job_counts.get(JobStatus.queued, 0),
            in_progress_jobs=job_counts.get(JobStatus.in_progress, 0),
            deferred_jobs=job_counts.get(JobStatus.deferred, 0),
            complete_jobs=job_counts.get(JobStatus.complete, 0),
            not_found_jobs=job_counts.get(JobStatus.not_found, 0),
        )

    async def get_job_by_id(
        self, job_id: str, redis: ArqRedis | None = None
    ) -> schemas.JobInfo:
        if redis is None:
            async with get_redis(self.redis_settings) as redis:
                return await self._get_job_by_id(redis, job_id)
        return await self._get_job_by_id(redis, job_id)

    async def _get_job_by_id(
        self, redis: ArqRedis, job_id: str
    ) -> schemas.JobInfo:
        arq_job = ArqJob(
            job_id=job_id,
            redis=redis,
            _queue_name=self.name,
            _deserializer=settings.arq_deserializer,
        )

        unknown_function_msg = "unknown"
        base_info: JobDef | schemas.JobDef | None = None

        try:
            base_info = await arq_job.info()
        except DeserializationError:
            unknown_function_msg = "unknown (unable to deserialize job)"

        if not base_info:
            base_info = schemas.JobDef(
                function=unknown_function_msg,
                args=(),
                kwargs={},
                job_try=-1,
            )

        job_info = schemas.JobInfo.from_base(base_info, job_id)
        job_info.status = await arq_job.status()
        return job_info

    async def _get_job_status(self, redis: ArqRedis, job_id: str) -> JobStatus:
        arq_job = ArqJob(
            job_id=job_id,
            redis=redis,
            _queue_name=self.name,
            _deserializer=settings.arq_deserializer,
        )
        return await arq_job.status()

    async def _filter_job_by_status(
        self, redis: ArqRedis, job_id: str, status: JobStatus
    ):
        if status == await self._get_job_status(redis, job_id):
            return job_id
        return None
