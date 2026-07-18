from pathlib import Path
from loguru import logger
import sys

base_dir = Path(__file__).parent.parent


def setup_logging():
    # Remove Loguru's default handler (which logs to stderr) so we control sinks
    logger.remove()

    try:
        logger.add(
            base_dir / "logs" / "info.log",
            format="{time} {level} {message}",
            level="INFO",
            rotation="1 MB",
        )

        logger.add(
            base_dir / "logs" / "error.log",
            format="{time} {level} {message}",
            level="ERROR",
            rotation="1 MB",
            filter=lambda record: (
                record["level"].name in ["WARNING", "ERROR", "CRITICAL"]
            ),
        )

        logger.add(
            base_dir / "logs" / "debug.log",
            format="{time} {level} {message}",
            level="DEBUG",
            rotation="1 MB",
        )

        logger.add(
            sys.stderr,
            format="{time} {level} {message}",
            level="WARNING",
        )

        return logger.bind(file_only=True)
    except Exception as e:
        print(e)
        pid_file = base_dir / "process.pid"
        try:
            pid_file.unlink()
        except FileNotFoundError:
            pass


setup_logging()
