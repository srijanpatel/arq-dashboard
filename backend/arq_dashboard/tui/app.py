import contextlib

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.design import ColorSystem
from textual.timer import Timer
from textual.widgets import DataTable, Footer, Header, Label, Static

from arq_dashboard.tui.data import DashboardData, fetch_all_data

# Warm earth-tone palette matching the web UI
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


class QueueCard(Static):
    """Single stat card."""

    def __init__(self, label: str, value: int = 0, style_class: str = ""):
        super().__init__()
        self._label = label
        self._slug = _slugify(label)
        self._value = value
        if style_class:
            self.add_class(style_class)

    def compose(self) -> ComposeResult:
        yield Label(str(self._value), id=f"val-{self._slug}", classes="card-value")
        yield Label(self._label, classes="card-label")

    def update_value(self, value: int):
        self._value = value
        with contextlib.suppress(Exception):
            self.query_one(f"#val-{self._slug}", Label).update(str(value))


class ThroughputCard(Static):
    """Throughput stat."""

    def __init__(self, label: str, value: str = "0", unit: str = ""):
        super().__init__()
        self._label = label
        self._value = value
        self._unit = unit
        self._id_safe = label.replace(" ", "-").lower()

    def compose(self) -> ComposeResult:
        yield Label(self._value, id=f"tp-{self._id_safe}", classes="card-value")
        yield Label(
            f"{self._unit}" if self._unit else self._label,
            classes="card-label",
        )

    def update_value(self, value: str):
        self._value = value
        with contextlib.suppress(Exception):
            self.query_one(f"#tp-{self._id_safe}", Label).update(value)


class ArqDashboardTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }

    #overview {
        height: auto;
        margin: 1 2;
    }

    #overview Horizontal {
        height: auto;
    }

    QueueCard {
        width: 1fr;
        height: 5;
        border: solid $primary-background;
        padding: 0 2;
        margin: 0 1;
        content-align: center middle;
    }

    QueueCard.queued { border: solid #8C7E72; }
    QueueCard.deferred { border: solid #5A9FD4; }
    QueueCard.in-progress { border: solid $primary; }
    QueueCard.complete { border: solid $success; }
    QueueCard.not-found { border: solid $warning; }

    .card-value {
        text-style: bold;
        width: 100%;
        text-align: center;
        color: $text;
    }

    .card-label {
        width: 100%;
        text-align: center;
        color: $text-muted;
    }

    #throughput {
        height: auto;
        margin: 1 2;
    }

    ThroughputCard {
        width: 1fr;
        height: 5;
        border: solid $accent;
        padding: 0 2;
        margin: 0 1;
        content-align: center middle;
    }

    #functions-section {
        margin: 1 2;
        height: 1fr;
    }

    #functions-section Label {
        margin: 0 0 1 0;
        text-style: bold;
    }

    DataTable {
        height: 1fr;
    }

    #status-bar {
        height: 1;
        dock: bottom;
        background: $primary-background;
        padding: 0 2;
    }
    """

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("d", "toggle_dark", "Toggle Dark/Light"),
        Binding("q", "quit", "Quit"),
    ]

    TITLE = "ARQ Dashboard"

    def __init__(self):
        super().__init__()
        self._refresh_timer: Timer | None = None
        self._data: DashboardData | None = None
        self.design = {"dark": WARM_DARK, "light": WARM_LIGHT}

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="overview"), Horizontal():
            yield QueueCard("Queued", style_class="queued")
            yield QueueCard("Deferred", style_class="deferred")
            yield QueueCard("In Progress", style_class="in-progress")
            yield QueueCard("Complete", style_class="complete")
            yield QueueCard("Not Found", style_class="not-found")

        with Container(id="throughput"), Horizontal():
            yield ThroughputCard("Throughput", "—", "jobs/min")
            yield ThroughputCard("Last 5min", "—", "completed")
            yield ThroughputCard("Last Hour", "—", "completed")

        with Vertical(id="functions-section"):
            yield Label("Function Performance")
            yield DataTable(id="fn-table")

        yield Label("Loading...", id="status-bar")
        yield Footer()

    async def on_mount(self):
        table = self.query_one("#fn-table", DataTable)
        table.add_columns(
            "Function", "Calls", "Success%", "Avg", "p50", "p95", "p99"
        )
        table.cursor_type = "row"

        await self.action_refresh()
        self._refresh_timer = self.set_interval(15, self.action_refresh)

    async def action_refresh(self):
        self._update_status("Refreshing...")
        try:
            self._data = await fetch_all_data()
            self._render_data()
            self._update_status(
                f"Last updated: {self._data.cached_at}  •  "
                f"Press [bold]r[/bold] to refresh"
            )
        except Exception as e:
            self._update_status(f"Error: {e}")

    def _render_data(self):
        if not self._data:
            return

        d = self._data

        # Update queue cards
        cards = self.query(QueueCard)
        values = [
            d.queued_jobs,
            d.deferred_jobs,
            d.in_progress_jobs,
            d.complete_jobs,
            d.not_found_jobs,
        ]
        for card, val in zip(cards, values, strict=False):
            card.update_value(val)

        # Update throughput
        tp_cards = list(self.query(ThroughputCard))
        if len(tp_cards) >= 3:
            tp_cards[0].update_value(str(d.throughput_per_min))
            tp_cards[1].update_value(str(d.jobs_last_5min))
            tp_cards[2].update_value(str(d.jobs_last_hour))

        # Update function table
        table = self.query_one("#fn-table", DataTable)
        table.clear()
        for fn in d.functions:
            rate = (
                f"{fn.success_count / fn.count * 100:.1f}%"
                if fn.count > 0
                else "—"
            )
            table.add_row(
                fn.function,
                str(fn.count),
                rate,
                self._fmt_ms(fn.avg_runtime_ms),
                self._fmt_ms(fn.p50_runtime_ms),
                self._fmt_ms(fn.p95_runtime_ms),
                self._fmt_ms(fn.p99_runtime_ms),
            )

    def _fmt_ms(self, ms: float) -> str:
        if ms == 0:
            return "—"
        if ms < 1000:
            return f"{int(ms)}ms"
        if ms < 60000:
            return f"{ms / 1000:.1f}s"
        return f"{ms / 60000:.1f}m"

    def _update_status(self, text: str):
        with contextlib.suppress(Exception):
            self.query_one("#status-bar", Label).update(text)
