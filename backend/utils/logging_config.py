import logging
import os
from pathlib import Path

def setup_logging():
    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(logs_dir / "app.log"),
            logging.StreamHandler()
        ]
    )