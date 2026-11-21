from datetime import datetime
from log_entry import LogEntry


def test_log_entry_creation():
    """Проверка создания объекта LogEntry.
    """
    
    timestamp = datetime(2026, 11, 21, 14, 30, 0)
    
    entry = LogEntry(
        timestamp=timestamp,
        level="ERROR",
        message="Database connection failed"
    )


    assert entry.timestamp == timestamp
    assert entry.level == "ERROR"
    assert entry.message == "Database connection failed"