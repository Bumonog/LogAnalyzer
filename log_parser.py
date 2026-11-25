from datetime import datetime
from log_entry import LogEntry

# Допустимые уровни важности лог-сообщений
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def parse_line(line: str) -> LogEntry | None:
    """
    Разбирает одну строку лог-файла.
    
    Возвращает обЪект LogEntry, если строка корректна.
    Возвращает None, если строка имеет неправильный формат.
    """
    
    # Разделяет строку на дату, время, уровень и текст сообщения
    parts = line.strip().split(maxsplit=3)
    
    # Проверяет, содержит ли строка все необходимые части
    if len(parts) != 4:
        return None
    
    date_part, time_part, level, message = parts
    
    # Проверяет, входит ли уровень сообщения в список допустимых
    if level not in LOG_LEVELS:
        return None
    # Преобразует дату и время в объект datetime
    try:
        timestamp = datetime.strptime(
            f"{date_part} {time_part}",
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        # Если дата или время указаны неправильно, отклоняем строку
        return None
    
    # Проверяем, что текст сообщения не пустой
    if not message.strip():
        return None
    
    # Создаём объект запис лог файла
    return LogEntry(
        timestamp=timestamp,
        level=level,
        message=message
    )


def parse_file(file_path: str) -> tuple[list[LogEntry], list[tuple[int, str]]]:
    """
    Читает лог-файл и разбирает его содержимое по строкам.
    
    Возвращает:
        Список корректных записей.
        Список некорректных строк с их номерами.
    """
    
    entries = []        # Список успешно обработанных записей
    invalid_lines = []  # Список строк с ошибками формата
    
    # Открывает файл для чтения в кодировке UTF-8
    with open(file_path, "r", encoding="utf-8") as file:
        
        # Перебирает строки файла, сохраняя их порядковые номера, начиная с 1
        for line_number, line in enumerate(file, start=1):
            entry = parse_line(line=line)
            
            # Корректные записи добавляются в основной список
            if entry is not None:
                entries.append(entry)
            
            # Некорректные непустые строки сохраняем отдельно
            elif line.strip():
                invalid_lines.append((line_number, line.strip()))
                
    return entries, invalid_lines