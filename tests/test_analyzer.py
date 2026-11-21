from datetime import datetime
from log_entry import LogEntry
from log_analyzer import analyze_logs, get_top_errors

timestamp = datetime(2026, 11, 21, 22, 38)


def test_analyze_logs():
    """Проверка подсчёта статистики."""

    entries = [
        LogEntry(None, "INFO", "Application started"),
        LogEntry(None, "WARNING", "High memory usage"),
        LogEntry(None, "ERROR", "Database error"),
        LogEntry(None, "CRITICAL", "Server unavailable"),
        LogEntry(None, "ERROR", "Database error"),
    ]

    result = analyze_logs(entries=entries)

    assert result["total"] == 5
    assert result["errors"] == 3
    assert result["warnings"] == 1
    assert result["levels"]["INFO"] == 1


def test_get_top_errors():
    """Проверка поиска наиболее частых ошибок."""

    entries = [
        LogEntry(None, "ERROR", "Database error"),
        LogEntry(None, "ERROR", "Database error"),
        LogEntry(None, "CRITICAL", "Server unavailable"),
    ]

    result = get_top_errors(entries)

    assert result[0] == ("Database error", 2)
    assert result[1] == ("Server unavailable", 1)


def test_get_top_errors_empty():
    """Проверка анализа списка без ошибок."""

    entries = [
        LogEntry(None, "INFO", "Application started"),
    ]

    assert get_top_errors(entries=entries) == []
