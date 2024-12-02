import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "/app/logs/app.log"
LOG_SIZE = 5 * 1024 * 1024

handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_SIZE, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
