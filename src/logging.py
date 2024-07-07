import queue
import logging
from logging.config import dictConfig
import logging.handlers

logger = logging.getLogger('AI App')

config = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "simple": {
      "format": "%(asctime)s | %(levelname)s | %{message}s"
    },
    "json": {
      "()": "src.utils.json_logger_util.JSONFormatter",
      "config": {

      }
    }
  },
  "handlers": {
    "stdout": {
      "class": "logging.StreamHandler",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    },
    "stderr": {
      "class": "logging.StreamHandler",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "json",
      "filename": "var/log/app.jsonl",
      "maxBytes": 1024 * 5,
      "backupCount": 3
    },
    "error-file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "WARNING",
      "formatter": "json",
      "filename": "var/log/app-errors.jsonl",
      "maxBytes": 1024 * 100,
      "backupCount": 3
    },
    "dev-file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "json",
      "filename": "var/log/dev.jsonl",
      "maxBytes": 1024 * 5,
      "backupCount": 3
    },
  },
  "loggers": {
    "developer": {
      "level": "DEBUG",
      "handlers": ["dev-file", "file"]
    }
  },
  "root": {
    "level": "DEBUG",
    "handlers": [ "file", "error-file" ]
  }
}

def initializeLogger():
  dictConfig(config=config)