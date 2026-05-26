export interface JobsWithPagination {
  jobs: Job[];
  total: number;
  currentPage: number;
  pageSize: number;
  cachedAt: string;
}

export interface Job {
  function: string;
  args: unknown[];
  kwargs: unknown;
  jobTry: number;
  enqueueTime: string | null;
  score: number | null;
  jobId: string;
  success: boolean;
  result: unknown;
  startTime: string | null;
  finishTime: string | null;
  queueName: string | null;
  status: string;
}

export interface CachedJob extends Job {
  cachedAt: string;
}

export interface Stats {
  name: string;
  host: string;
  port: number;
  database: number;
  queuedJobs: number;
  inProgressJobs: number;
  deferredJobs: number;
  completeJobs: number;
  notFoundJobs: number;
  cachedAt: string;
}

export interface SearchParams {
  functionName: string | undefined;
  startTime: string | undefined;
  finishTime: string | undefined;
  status: string | undefined;
  page: number;
  success: boolean | undefined;
}

export interface ItemName {
  name: string;
}

export type FunctionName = ItemName;
export type QueueName = ItemName;

// Function stats
export interface RuntimeBucket {
  rangeStartMs: number;
  rangeEndMs: number;
  count: number;
}

export interface FunctionRuntime {
  function: string;
  count: number;
  successCount: number;
  failureCount: number;
  avgRuntimeMs: number;
  p50RuntimeMs: number;
  p95RuntimeMs: number;
  p99RuntimeMs: number;
  minRuntimeMs: number;
  maxRuntimeMs: number;
  runtimeBuckets: RuntimeBucket[];
}

export interface FunctionStatsResponse {
  functions: FunctionRuntime[];
  cachedAt: string;
}
