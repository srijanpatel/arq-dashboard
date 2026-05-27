import contextlib
import json
from datetime import datetime

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.design import ColorSystem
from textual.screen import ModalScreen
from textual.timer import Timer
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Label,
    Static,
    TabbedContent,
    TabPane,
)

from arq_dashboard.tui.data import DashboardData, JobRow, fetch_all_data

WARM_DARK = ColorSystem(
    primary="#E09050",
    secondary="#A69B90",
    accent="#E09050",
    background="#1C1917",
    surface="#252220",
    panel="#302C29",
    warning="#D4A017",
    error="#D4635A",
    success="#6BA34A",
    dark=True,
)

WARM_LIGHT = ColorSystem(
    primary="#C8642A",
    secondary="#8C7E72",
    accent="#C8642A",
    background="#FAF6F1",
    surface="#F3EDE5",
    panel="#EBE3D9",
    warning="#B8860B",
    error="#C44B3F",
    success="#5A8A3C",
    dark=False,
)


def _slugify(s: str) -> str:
    return s.lower().replace(" ", "-")


def _fmt_ms(ms: float) -> str:
    if ms == 0:
        return "—"
    if ms < 1000:
        return f"{int(ms)}ms"
    if ms < 60000:
        return f"{ms / 1000:.1f}s"
    return f"{ms / 60000:.1f}m"


def _bar(fraction: float, width: int = 15) -> str:
    """Render a text-based progress bar."""
    filled = int(fraction * width)
    return "█" * filled + "░" * (width - filled)


def _duration_between(a: datetime | None, b: datetime | None) -> str:
    if a is None or b is None:
        return "—"
    return _fmt_ms((b - a).total_seconds() * 1000)


def _fmt_dt(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _pretty(value) -> str:
    """Best-effort JSON formatting of args/kwargs/result."""
    if value is None:
        return "null"
    if isinstance(value, tuple):
        value = list(value)
    try:
        return json.dumps(value, indent=2, default=str)
    except (TypeError, ValueError):
        return repr(value)


class StatRow(Static):
    """Compact horizontal row of stat values."""

    DEFAULT_CSS = """
    StatRow {
        height: 3;
        margin: 0 1;
        padding: 0 1;
    }
    StatRow Horizontal {
        height: auto;
    }
    StatRow .stat-item {
        width: 1fr;
        height: 3;
        content-align: center middle;
        text-align: center;
    }
    StatRow .stat-val {
        text-style: bold;
        width: 100%;
        text-align: center;
    }
    StatRow .stat-lbl {
        width: 100%;
        text-align: center;
        color: $text-muted;
    }
    """

    def __init__(self, items: list[tuple[str, str, str]]):
        """items: list of (id_suffix, value, label)"""
        super().__init__()
        self._items = items

    def compose(self) -> ComposeResult:
        with Horizontal():
            for id_suffix, value, label in self._items:
                with Static(classes="stat-item"):
                    yield Label(
                        value,
                        id=f"sv-{id_suffix}",
                        classes="stat-val",
                    )
                    yield Label(label, classes="stat-lbl")

    def update_item(self, id_suffix: str, value: str):
        with contextlib.suppress(Exception):
            self.query_one(f"#sv-{id_suffix}", Label).update(value)


class JobDetailScreen(ModalScreen):
    """Modal showing full details for a single job."""

    CSS = """
    JobDetailScreen {
        align: center middle;
    }

    #detail-box {
        width: 90%;
        max-width: 100;
        height: 90%;
        background: $surface;
        border: round $accent;
        padding: 1 2;
    }

    #detail-box .detail-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    #detail-box .field-label {
        color: $text-muted;
        text-style: bold;
        margin: 1 0 0 0;
    }

    #detail-box .field-value {
        margin: 0 0 1 1;
    }

    #detail-box .code-block {
        background: $panel;
        padding: 1 2;
        margin: 0 0 1 1;
        border-left: thick $accent;
    }

    #detail-tags {
        height: auto;
        margin-bottom: 1;
    }

    #detail-tags .tag {
        background: $panel;
        padding: 0 1;
        margin-right: 1;
    }

    #timeline-row {
        height: auto;
        margin: 1 0;
    }

    .timeline-step {
        width: 1fr;
        height: auto;
        content-align: center top;
        text-align: center;
    }

    .timeline-dot {
        color: $accent;
        text-style: bold;
        text-align: center;
    }

    .timeline-arrow {
        width: auto;
        color: $text-muted;
        content-align: center middle;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
    ]

    def __init__(self, job: JobRow):
        super().__init__()
        self._job = job

    def compose(self) -> ComposeResult:
        job = self._job
        success_tag = "✓ success" if job.success else "✗ failure"

        with ScrollableContainer(id="detail-box"):
            yield Label(f"Job  {job.job_id}", classes="detail-title")

            with Horizontal(id="detail-tags"):
                yield Label(f" {job.status} ", classes="tag")
                yield Label(f" {success_tag} ", classes="tag")
                if job.job_try is not None and job.job_try > 1:
                    yield Label(f" try #{job.job_try} ", classes="tag")

            wait = _duration_between(job.enqueue_time_dt, job.start_time_dt)
            run = _duration_between(job.start_time_dt, job.finish_time_dt)

            yield Label("TIMELINE", classes="field-label")
            with Horizontal(id="timeline-row"):
                yield Static(
                    f"● Enqueued\n{_fmt_dt(job.enqueue_time_dt)}",
                    classes="timeline-step",
                )
                yield Label(f"── {wait} wait ──", classes="timeline-arrow")
                yield Static(
                    f"● Started\n{_fmt_dt(job.start_time_dt)}",
                    classes="timeline-step",
                )
                yield Label(f"── {run} runtime ──", classes="timeline-arrow")
                yield Static(
                    f"● Finished\n{_fmt_dt(job.finish_time_dt)}",
                    classes="timeline-step",
                )

            yield Label("FUNCTION", classes="field-label")
            yield Label(job.function, classes="field-value")

            yield Label("QUEUE", classes="field-label")
            yield Label(job.queue_name, classes="field-value")

            yield Label("ARGS", classes="field-label")
            yield Static(_pretty(job.args), classes="code-block")

            yield Label("KWARGS", classes="field-label")
            yield Static(_pretty(job.kwargs), classes="code-block")

            yield Label("RESULT", classes="field-label")
            yield Static(_pretty(job.result), classes="code-block")

            yield Label("[dim]Press Esc to close[/dim]")


class ArqDashboardTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }

    TabbedContent {
        margin: 0 1;
    }

    #stats-pane, #jobs-pane {
        padding: 0;
    }

    DataTable {
        height: 1fr;
    }

    #status-bar {
        height: 1;
        dock: bottom;
        background: $primary-background;
        padding: 0 2;
        color: $text-muted;
    }

    .section-title {
        margin: 1 1 0 1;
        text-style: bold;
        color: $accent;
    }
    """

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("d", "toggle_dark", "Dark/Light"),
        Binding("1", "tab_stats", "Stats", show=False),
        Binding("2", "tab_jobs", "Jobs", show=False),
        Binding("q", "quit", "Quit"),
    ]

    TITLE = "ARQ Dashboard"

    def __init__(self, data_fetcher=None):
        super().__init__()
        self._refresh_timer: Timer | None = None
        self._data: DashboardData | None = None
        self._data_fetcher = data_fetcher or fetch_all_data
        self.design = {"dark": WARM_DARK, "light": WARM_LIGHT}

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent("Stats", "Jobs"):
            with TabPane("Stats", id="stats-pane"), ScrollableContainer():
                yield Label(" Queue Overview", classes="section-title")
                yield StatRow(
                    [
                        ("queued", "0", "Queued"),
                        ("deferred", "0", "Deferred"),
                        ("in-progress", "0", "In Progress"),
                        ("complete", "0", "Complete"),
                        ("not-found", "0", "Not Found"),
                    ]
                )
                yield Label(" Throughput", classes="section-title")
                yield StatRow(
                    [
                        ("tpm", "—", "jobs/min"),
                        ("t5m", "—", "last 5 min"),
                        ("t1h", "—", "last hour"),
                    ]
                )
                yield Label(" Function Performance", classes="section-title")
                yield DataTable(id="fn-table")

            with TabPane("Jobs", id="jobs-pane"):
                yield DataTable(id="jobs-table")

        yield Label("Loading...", id="status-bar")
        yield Footer()

    async def on_mount(self):
        # Function performance table
        fn_table = self.query_one("#fn-table", DataTable)
        fn_table.add_columns(
            "Function",
            "Calls",
            "Success",
            "Rate",
            "Avg",
            "p50",
            "p95",
            "p99",
        )
        fn_table.cursor_type = "row"

        # Jobs table
        jobs_table = self.query_one("#jobs-table", DataTable)
        jobs_table.add_columns(
            "Job ID",
            "Function",
            "Status",
            "Success",
            "Queue",
            "Enqueued",
            "Runtime",
        )
        jobs_table.cursor_type = "row"

        await self.action_refresh()
        self._refresh_timer = self.set_interval(15, self.action_refresh)

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id != "jobs-table" or not self._data:
            return
        row_index = event.cursor_row
        if 0 <= row_index < len(self._data.jobs):
            self.push_screen(JobDetailScreen(self._data.jobs[row_index]))

    def action_tab_stats(self):
        with contextlib.suppress(Exception):
            self.query_one(TabbedContent).active = "stats-pane"

    def action_tab_jobs(self):
        with contextlib.suppress(Exception):
            self.query_one(TabbedContent).active = "jobs-pane"

    async def action_refresh(self):
        self._update_status("⟳ Refreshing...")
        try:
            self._data = await self._data_fetcher()
            self._render_data()
            self._update_status(
                f"Updated {self._data.cached_at}  •  "
                f"r=refresh  d=theme  1=stats  2=jobs  ↵=details  q=quit"
            )
        except Exception as e:
            self._update_status(f"Error: {e}")

    def _render_data(self):
        if not self._data:
            return
        d = self._data

        # Queue overview
        overview = self.query(StatRow).first()
        if overview:
            overview.update_item("queued", str(d.queued_jobs))
            overview.update_item("deferred", str(d.deferred_jobs))
            overview.update_item("in-progress", str(d.in_progress_jobs))
            overview.update_item("complete", str(d.complete_jobs))
            overview.update_item("not-found", str(d.not_found_jobs))

        # Throughput
        tp_row = list(self.query(StatRow))
        if len(tp_row) >= 2:
            tp_row[1].update_item("tpm", str(d.throughput_per_min))
            tp_row[1].update_item("t5m", str(d.jobs_last_5min))
            tp_row[1].update_item("t1h", str(d.jobs_last_hour))

        # Function table
        fn_table = self.query_one("#fn-table", DataTable)
        fn_table.clear()
        for fn in d.functions:
            rate = fn.success_count / fn.count if fn.count > 0 else 0
            fn_table.add_row(
                fn.function,
                str(fn.count),
                f"{fn.success_count}/{fn.count}",
                f"{_bar(rate)} {rate * 100:.0f}%",
                _fmt_ms(fn.avg_runtime_ms),
                _fmt_ms(fn.p50_runtime_ms),
                _fmt_ms(fn.p95_runtime_ms),
                _fmt_ms(fn.p99_runtime_ms),
            )

        # Jobs table
        jobs_table = self.query_one("#jobs-table", DataTable)
        jobs_table.clear()
        for job in d.jobs:
            runtime = _fmt_ms(job.runtime_ms) if job.runtime_ms else "—"
            jobs_table.add_row(
                job.job_id[:12],
                job.function,
                job.status,
                "✓" if job.success else "✗",
                job.queue_name,
                job.enqueue_time,
                runtime,
            )

    def _update_status(self, text: str):
        with contextlib.suppress(Exception):
            self.query_one("#status-bar", Label).update(text)
