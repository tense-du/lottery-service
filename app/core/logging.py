"""Simple logging configuration."""

import logging
from pathlib import Path
from app.core.settings import settings

# Create logs directory under app/ if it doesn't exist
log_dir = Path("app/logs")
log_dir.mkdir(exist_ok=True)

# Basic logging setup
logging.basicConfig(
    level=logging.WARNING,  # Only capture WARNING and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'lottery_service.log'),
        logging.StreamHandler()  # Console output
    ]
)

# Create logger
logger = logging.getLogger('lottery_service') 