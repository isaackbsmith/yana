import json
from logging import Formatter, LogRecord
import datetime as dt


class JSONFormatter(Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys else {}

    def format(self, record: LogRecord) -> str:
        log_data = {
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
            "module": record.module,
            "func_name": record.funcName,
            "line_number": record.lineno,
        }
        return json.dumps(log_data, default=str)
