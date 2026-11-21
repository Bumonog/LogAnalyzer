from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    """
    Класс для хранения одной записи лог-файла.
    
    Attributes:
        timestamp (datetime): Дата и время события.
        level (str): Уровень важности события.
        message (str): Текст лог-события.
    
    """
    
    timestamp: datetime  # Дата и время возникновения события
    level: str           # Уровень важности: INFO, WARNING, ERROR и т. д.
    message: str         # Содержание сообщения