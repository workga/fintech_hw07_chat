import logging

from app.settings import app_settings

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter(
        '%(levelname)s %(asctime)s %(funcName)s(%(lineno)d) %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
    )
)

logger = logging.getLogger(app_settings.logger_name)
logger.addHandler(stream_handler)
logger.setLevel(app_settings.logger_level)
