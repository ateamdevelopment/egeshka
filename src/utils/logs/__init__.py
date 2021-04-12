import json
import logging
from logging.config import dictConfig

from src.utils.logs._cache_message_log_record import CacheMessageLogRecord
from src.utils.logs._logs_drainer import LogsDrainer

__all__ = ['init_loggers']

logging.setLogRecordFactory(CacheMessageLogRecord)


def init_loggers() -> None:
    path_to_config = 'src/utils/logs/config.json'
    with open(path_to_config, 'r') as logs_config_json:
        logs_config = json.load(logs_config_json)
    dictConfig(logs_config)
    LogsDrainer('/src/utils/logs/logs.log')
