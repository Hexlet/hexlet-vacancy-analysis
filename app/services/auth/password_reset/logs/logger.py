import logging
from app.services.auth.password_reset import configs

log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "NOTSET": logging.NOTSET,
}

logging.basicConfig(
    filename=configs.LOG_FILE,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
    level=log_levels[configs.LOG_LEVEL],
)
