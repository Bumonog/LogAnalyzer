from datetime import datetime
from log_entry import LogEntry
from log_parser import parse_line, parse_file


def test_parse_valid_line():
    """Проверка разбора корректной строки."""
    
    # Строка с правильным форматом
    line = "2026-11-20 10:15:32 ERROR Database connection failed"
    
    # Передача строки парсеру
    entry = parse_line(line=line)
    
    # Проверка правильности полученных данных
    assert isinstance(entry, LogEntry)
    assert entry.timestamp == datetime(2026, 11, 20, 10, 15, 32)
    assert entry.level == "ERROR"
    assert entry.message == "Database connection failed"


def test_parse_invalid_date():
    """Проверка строки с неправильной датой."""

    # Строка с неправильной датой(15-й месяц)
    line = "2026-15-20 10:15:32 ERROR Database error"

    assert parse_line(line=line) is None


def test_parse_invalid_level():
    """Проверка строки с неизвестным уровнем."""
    
    # Строка с неизвестным уровнем сообщения
    line = "2026-11-20 10:15:32 UNKNOWN Something happened"
    
    assert parse_line(line=line) is None


def test_parse_empty_message():
    """Проверка отсутствующего текста сообщения."""
    
    # Строка без текста сообщения
    line = "2026-11-20 10:15:32 ERROR"
    
    assert parse_line(line=line) is None


def test_empty_line():
    """Проверка пустой строки."""
    
    assert parse_line(line="") is None


def test_parse_file():
    """Проверка обработки текстового лог-файла."""
    
    # Парсинг файла sample.log
    entries, invalid_lines = parse_file(file_path="data/sample.log")
    
    assert len(entries) == 7         # Проверка успешно обработанных записей
    assert len(invalid_lines) == 1   # Проверка строк с ошибками формата
    assert invalid_lines[0][0] == 7  # Проверк номера некорректной строки