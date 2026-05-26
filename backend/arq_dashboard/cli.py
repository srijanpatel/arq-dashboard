
import click


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """ARQ Dashboard — monitoring for ARQ job queues."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(web)


@main.command()
@click.option("--host", default="0.0.0.0", help="Bind host")
@click.option("--port", default=8000, type=int, help="Bind port")
def web(host, port):
    """Launch the web dashboard (default)."""
    import uvicorn

    uvicorn.run("arq_dashboard:app", host=host, port=port)


@main.command()
def tui():
    """Launch the terminal UI dashboard."""
    from arq_dashboard.tui.app import ArqDashboardTUI

    app = ArqDashboardTUI()
    app.run()
