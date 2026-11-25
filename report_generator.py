import json
from datetime import datetime
from pathlib import Path

def generate_txt_report(
    statistics: dict,
    top_errors: list[tuple[str, int]],
    invalid_count: int,
    output_path: str
) -> None:
    """Формирует текстовый отчёт и сохраняет его в файле."""
    
    # Создаём список строк будущего отчёта
    lines = [
        "ОТЧЁТ ПО РЕЗУЛЬТАТАМ АНАЛИЗА ЛОГ-ФАЙЛОВ",
        "=" * 45,
        f"Дата формирования: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        f"Всего записей: {statistics['total']}",
        f"Количество ошибок: {statistics['errors']}",
        f"Количество предупреждений: {statistics['warnings']}",
        f"Некорректных строк: {invalid_count}",
        "",
        "СТАТИСТИКА ПО УРОВНЯМ:",
    ]
    
    # Добавляет количество сообщений каждого уровня
    for level, count in statistics['levels'].items():
        lines.append(f"{level}: {count}")
        
    # Добавляет информацию о наиболее частых ошибках
    lines.extend(["", "НАИБОЛЕЕ ЧАСТЫЕ ОШИБКИ:"])
    
    if top_errors:
        for message, count in top_errors:
            lines.append(f"{message} - {count} раз.")
    
    else:
        lines.append("Ошибок не обнаружено.")
        
    # Объединяет строки в один текст
    report_text = "\n".join(lines)
    
    # Сохраняет отчёт в файл
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")
    
    
def generate_json_report(
    statistics: dict,
    top_errors: list[tuple[str, int]],
    invalid_count: int,
    output_path: str
    ) -> None:
        """Формирует JSON-отчёт и сохраняет его в файл."""
        
        # Подгатавливает данные для JSON-отчёта
        report_data = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "statistics": statistics,
            "top_errors": [
                {"message": message, "count": count}
                for message, count in top_errors
            ],
            "invalid_lines_count": invalid_count,
        }
        
        # Создаёт папку для отчёта, если она отсутствует
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Записывает данные в JSON-файл
        with path.open("w", encoding="utf-8") as file:
            json.dump(
                report_data,
                file,
                ensure_ascii=False,
                indent=4
            )