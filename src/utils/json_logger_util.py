import logging
import json
from datetime import datetime, UTC
from typing import Optional
from src.utils.logging_utils import getLogMetadata

class JSONFormatter(logging.Formatter):
  def __init__(self, *, config: Optional[dict[str, str]] = None):
    super().__init__()
    self.config = config if config is not None else {}

  def format(self, record: logging.LogRecord):
    message = self._prepare_log_dict(record)
    return json.dumps(message, default=str)

  def _prepare_log_dict(self, record: logging.LogRecord):
    data = {
      "logger": record.name,
      "level": record.levelname,
      "message": record.getMessage(),
      "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat()
    }

    message = {
      key: msg_val
      if (msg_val := data.pop(val, None)) is not None
      else getattr(record, val)
      for key,val in self.config.items()
    }

    getLogMetadata(record, message)

    message.update(data)

    return message