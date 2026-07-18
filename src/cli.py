import typer
import subprocess
import sys
import os
import signal
from pathlib import Path
from loguru import logger

try:
    from .log_manager import setup_logging
except ImportError:
    from log_manager import setup_logging

setup_logging()

base_dir = Path(__file__).parent.parent
pid_file = base_dir / "process.pid"

app = typer.Typer()


@app.command()
def start():
    """Starts Tracker's tracking process"""
    if pid_file.exists():
        if pid_file.read_text():
            logger.info("Tracker is already running")
            raise typer.Exit()
        else:
            logger.warning("Tracker have not started but pid_file exists")
            pid_file.unlink()
    typer.echo("starting Tracker")
    logger.info("starting Tracker...")

    process = subprocess.Popen([sys.executable, base_dir / "src" / "main.py"])
    pid_file.write_text(str(process.pid))
    logger.info(f"Process started successfully with PID: {process.pid}")
    raise typer.Exit()


@app.command()
def stop():
    """Stops Tracker's tracking process"""
    if not pid_file.exists():
        logger.info("Tracker is not running")
        raise typer.Exit()
    try:
        logger.info("stopping Tracker...")
        pid = int(pid_file.read_text().rstrip())
        os.kill(pid, signal.SIGTERM)
        pid_file.unlink()
        logger.info("Tracker procces stopped successfully.")
    except ProcessLookupError:
        logger.warning(
            "Process was not running, but a stale PID file was found. Cleaning up."
        )
        pid_file.unlink()
    except PermissionError:
        logger.error("You do not have permission to stop this process.")


# @app.command()
# def hello(name: str):
#     print(f"Hello {name}")


# @app.command()
# def goodbye(name: str, formal: bool = False):
#     if formal:
#         print(f"Goodbye Ms. {name}. Have a good day.")
#     else:
#         print(f"Bye {name}!")


if __name__ == "__main__":
    app()
