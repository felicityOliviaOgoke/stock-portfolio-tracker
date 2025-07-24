import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs/ directory if it doesn't exist
log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "app.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3),
        logging.StreamHandler(sys.stdout),
    ]
)

# Optional: custom log() shortcut to replace print()
def log(msg, level="info"):
    print(msg)
    getattr(logging, level.lower(), logging.info)(msg)

# Log uncaught exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if not issubclass(exc_type, KeyboardInterrupt):
        logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
