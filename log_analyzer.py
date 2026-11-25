from collections import Counter
from log_entry import LogEntry


def analyze_logs(entries: list[LogEntry]) -> dict:
    """
    Выполняет анализ списка записей лог-файла.
    
    Возвращяет словарь со статисттикой:
        общее кол-во записей, кол-во сообщений
        каждого уровня, ошибки и предупреждения.
    """
    
    # Подсчитывает кол-во сообщений каждого уровня
    level_counts = Counter(entry.level for entry in entries)
    
    # Вычисляет общее кол-во ошибок(ERROR + CRITICAL)
    error_count = level_counts["ERROR"] + level_counts["CRITICAL"]
    
    # Вычисляет общее кол-во предупреждений(WARNING)
    warning_count = level_counts["WARNING"]
    
    # Формирует итоговую статистику
    statistics = {
        "total": len(entries),
        "levels": dict(level_counts),
        "errors": error_count,
        "warnings": warning_count,
    }
    
    return statistics


def get_top_errors( 
    entries: list[LogEntry],
    limit: int = 5
) -> list[tuple[str, int]]:
    """
    Находит наиболее часто встречающиеся сообщения об ошибках.
    """
    
    # Отбирает сообщения уровней ERROR и CRITICAL
    error_messages = [entry.message for entry in entries if entry.level in ("ERROR", "CRITICAL")]
    
    # Подсчитывает частоту повторения сообщений
    error_counts = Counter(error_messages)
    
    # Возвращает наиболее частые сообщения
    return error_counts.most_common(limit)