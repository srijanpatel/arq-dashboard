"""Mock backend serving realistic fake data for screenshots."""

import json
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler

NOW = datetime.now(timezone.utc)


def mock_stats():
    return {
        "cachedAt": NOW.isoformat(),
        "name": "arq:queue",
        "host": "redis-prod.example.com",
        "port": 6379,
        "database": 0,
        "queuedJobs": 12,
        "inProgressJobs": 7,
        "deferredJobs": 3,
        "completeJobs": 4821,
        "notFoundJobs": 0,
    }


def mock_function_stats():
    return {
        "cachedAt": NOW.isoformat(),
        "throughput": {
            "jobsLastHour": 847,
            "jobsLast5min": 73,
            "throughputPerMin": 14.12,
        },
        "functions": [
            {
                "function": "send_notification",
                "count": 2134,
                "successCount": 2098,
                "failureCount": 36,
                "avgRuntimeMs": 245.3,
                "p50RuntimeMs": 180.0,
                "p95RuntimeMs": 620.5,
                "p99RuntimeMs": 1250.0,
                "minRuntimeMs": 45.0,
                "maxRuntimeMs": 3200.0,
                "runtimeBuckets": [
                    {"rangeStartMs": 45, "rangeEndMs": 360, "count": 890},
                    {"rangeStartMs": 360, "rangeEndMs": 675, "count": 620},
                    {"rangeStartMs": 675, "rangeEndMs": 990, "count": 310},
                    {"rangeStartMs": 990, "rangeEndMs": 1305, "count": 145},
                    {"rangeStartMs": 1305, "rangeEndMs": 1620, "count": 82},
                    {"rangeStartMs": 1620, "rangeEndMs": 1935, "count": 41},
                    {"rangeStartMs": 1935, "rangeEndMs": 2250, "count": 22},
                    {"rangeStartMs": 2250, "rangeEndMs": 2565, "count": 14},
                    {"rangeStartMs": 2565, "rangeEndMs": 2880, "count": 7},
                    {"rangeStartMs": 2880, "rangeEndMs": 3200, "count": 3},
                ],
            },
            {
                "function": "process_payment",
                "count": 1456,
                "successCount": 1432,
                "failureCount": 24,
                "avgRuntimeMs": 1823.7,
                "p50RuntimeMs": 1540.0,
                "p95RuntimeMs": 3800.0,
                "p99RuntimeMs": 5200.0,
                "minRuntimeMs": 320.0,
                "maxRuntimeMs": 8500.0,
                "runtimeBuckets": [
                    {"rangeStartMs": 320, "rangeEndMs": 1138, "count": 280},
                    {"rangeStartMs": 1138, "rangeEndMs": 1956, "count": 520},
                    {"rangeStartMs": 1956, "rangeEndMs": 2774, "count": 340},
                    {"rangeStartMs": 2774, "rangeEndMs": 3592, "count": 165},
                    {"rangeStartMs": 3592, "rangeEndMs": 4410, "count": 78},
                    {"rangeStartMs": 4410, "rangeEndMs": 5228, "count": 38},
                    {"rangeStartMs": 5228, "rangeEndMs": 6046, "count": 18},
                    {"rangeStartMs": 6046, "rangeEndMs": 6864, "count": 10},
                    {"rangeStartMs": 6864, "rangeEndMs": 7682, "count": 5},
                    {"rangeStartMs": 7682, "rangeEndMs": 8500, "count": 2},
                ],
            },
            {
                "function": "generate_report",
                "count": 892,
                "successCount": 871,
                "failureCount": 21,
                "avgRuntimeMs": 12450.0,
                "p50RuntimeMs": 10200.0,
                "p95RuntimeMs": 24500.0,
                "p99RuntimeMs": 38000.0,
                "minRuntimeMs": 2100.0,
                "maxRuntimeMs": 45000.0,
                "runtimeBuckets": [
                    {"rangeStartMs": 2100, "rangeEndMs": 6390, "count": 180},
                    {"rangeStartMs": 6390, "rangeEndMs": 10680, "count": 310},
                    {"rangeStartMs": 10680, "rangeEndMs": 14970, "count": 195},
                    {"rangeStartMs": 14970, "rangeEndMs": 19260, "count": 98},
                    {"rangeStartMs": 19260, "rangeEndMs": 23550, "count": 52},
                    {"rangeStartMs": 23550, "rangeEndMs": 27840, "count": 28},
                    {"rangeStartMs": 27840, "rangeEndMs": 32130, "count": 15},
                    {"rangeStartMs": 32130, "rangeEndMs": 36420, "count": 8},
                    {"rangeStartMs": 36420, "rangeEndMs": 40710, "count": 4},
                    {"rangeStartMs": 40710, "rangeEndMs": 45000, "count": 2},
                ],
            },
            {
                "function": "sync_inventory",
                "count": 339,
                "successCount": 339,
                "failureCount": 0,
                "avgRuntimeMs": 4560.0,
                "p50RuntimeMs": 3800.0,
                "p95RuntimeMs": 8900.0,
                "p99RuntimeMs": 12000.0,
                "minRuntimeMs": 1200.0,
                "maxRuntimeMs": 15000.0,
                "runtimeBuckets": [
                    {"rangeStartMs": 1200, "rangeEndMs": 2580, "count": 45},
                    {"rangeStartMs": 2580, "rangeEndMs": 3960, "count": 120},
                    {"rangeStartMs": 3960, "rangeEndMs": 5340, "count": 85},
                    {"rangeStartMs": 5340, "rangeEndMs": 6720, "count": 42},
                    {"rangeStartMs": 6720, "rangeEndMs": 8100, "count": 22},
                    {"rangeStartMs": 8100, "rangeEndMs": 9480, "count": 12},
                    {"rangeStartMs": 9480, "rangeEndMs": 10860, "count": 7},
                    {"rangeStartMs": 10860, "rangeEndMs": 12240, "count": 4},
                    {"rangeStartMs": 12240, "rangeEndMs": 13620, "count": 1},
                    {"rangeStartMs": 13620, "rangeEndMs": 15000, "count": 1},
                ],
            },
        ],
    }


STATUSES = ["complete", "in_progress", "queued", "deferred"]
FUNCTIONS = [
    "send_notification",
    "process_payment",
    "generate_report",
    "sync_inventory",
]


def mock_jobs():
    jobs = []
    for i in range(25):
        status = "complete" if i > 3 else STATUSES[i]
        func = FUNCTIONS[i % len(FUNCTIONS)]
        enqueue = NOW - timedelta(minutes=50 - i * 2)
        start = enqueue + timedelta(seconds=1) if status != "queued" else None
        finish = (
            start + timedelta(seconds=[0.2, 1.8, 12.4, 4.5][i % 4])
            if status == "complete" and start
            else None
        )
        jobs.append(
            {
                "function": func,
                "args": ["usr_" + f"{1000+i}", "ctx_" + f"{5000+i}"],
                "kwargs": {},
                "jobTry": 1 if i != 5 else 3,
                "enqueueTime": enqueue.isoformat(),
                "score": int(enqueue.timestamp() * 1000),
                "jobId": f"a{i:02d}b{i*7:04d}c{i*13:04d}d{i*3:04d}e{i*11:04d}",
                "success": status == "complete",
                "queueName": "arq:queue",
                "result": "ok" if status == "complete" else None,
                "startTime": start.isoformat() if start else None,
                "finishTime": finish.isoformat() if finish else None,
                "status": status,
            }
        )
    return {
        "total": 4821,
        "pageSize": 100,
        "currentPage": 1,
        "cachedAt": NOW.isoformat(),
        "jobs": jobs,
    }


def mock_single_job():
    enqueue = NOW - timedelta(minutes=12)
    start = enqueue + timedelta(seconds=0.8)
    finish = start + timedelta(seconds=1.82)
    return {
        "function": "process_payment",
        "args": ["usr_1042", "ord_88291"],
        "kwargs": {"currency": "USD", "amount": 49.99, "retry": False},
        "jobTry": 1,
        "enqueueTime": enqueue.isoformat(),
        "score": int(enqueue.timestamp() * 1000),
        "jobId": "a03b0021c0039d0009e0033",
        "success": True,
        "queueName": "arq:queue",
        "result": {"transactionId": "txn_9f8a7b6c", "status": "settled"},
        "startTime": start.isoformat(),
        "finishTime": finish.isoformat(),
        "status": "complete",
        "cachedAt": NOW.isoformat(),
    }


def mock_functions():
    return [{"name": f} for f in FUNCTIONS]


def mock_queues():
    return [{"name": "arq:queue"}]


class MockHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/api/stats/": mock_stats,
            "/api/stats/functions/": mock_function_stats,
            "/api/jobs/": mock_jobs,
            "/api/functions/": mock_functions,
            "/api/queues/": mock_queues,
        }

        path = self.path.split("?")[0]

        # Match single job route
        if path.startswith("/api/jobs/") and path != "/api/jobs/":
            data = mock_single_job()
        else:
            handler = routes.get(path)
            if not handler:
                self.send_response(404)
                self.end_headers()
                return
            data = handler()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # Silence logs


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 9999), MockHandler)
    print("Mock server on http://127.0.0.1:9999")
    server.serve_forever()
