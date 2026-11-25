from pathlib import Path

from log_parser import parse_file
from log_analyzer import analyze_logs, get_top_errors
from report_generator import (
    generate_txt_report,
    generate_json_report
)


def show_menu():
    """Отображает главное меню программы"""
    
    print("\n" + "=" * 45)
    print("       АНАЛИЗАТОР ЛОГ-ФАЙЛОВ")
    print("=" * 45)
    print("1. Анализировать лог-файл")
    print("2. Выход")
    print("=" * 45)


def analyze_file():
    """Выполняет анализ выбранного лог-файла."""
    
    file_path = input("Введите путь к лог-файлу: ").strip()
    
    path = Path(file_path)
    
    if not path.exists():
        print("Ошибка: указанный файл не найден.")
        return
    
    if not path.is_file():
        print("Ошибка: указанный  путь не является файлом.")
        return
    
    try:
        entries, invalid_lines = parse_file(str(path))
        
        statistics = analyze_logs(entries)
        top_errors = get_top_errors(entries)
        
        print("\nРЕЗУЛЬТАТЫ АНАЛИЗА")
        print("-" * 35)
        print(f"Всего записей: {statistics['total']}")
        print(f"Ошибок: {statistics['errors']}")
        print(f"Предупреждений: {statistics['warnings']}")
        print(f"Некорректных строк: {len(invalid_lines)}")

        print("\nНаиболее частые ошибки:")

        if top_errors:
            for message, count in top_errors:
                print(f"{message} — {count} раз.")
        else:
            print("Ошибок не обнаружено.")
        
        # Выбор формата отчёта для сохранения/ не сохранять    
        print("\nСОХРАНЕНИЕ ОТЧЁТА")
        print("1. Текстовый файл (TXT)")
        print("2. Файл JSON")
        print("3. Не сохранять отчёт")

        report_choice = input("Выберите формат отчёта: ").strip()

        if report_choice == "1":
            output_path = "reports/report.txt"

            generate_txt_report(
                statistics,
                top_errors,
                len(invalid_lines),
                output_path,
            )

            print(f"Отчёт сохранён: {output_path}")

        elif report_choice == "2":
            output_path = "reports/report.json"

            generate_json_report(
                statistics,
                top_errors,
                len(invalid_lines),
                output_path,
            )

            print(f"Отчёт сохранён: {output_path}")

        elif report_choice == "3":
            print("Отчёт не сохранялся.")

        else:
            print("Неверный выбор формата отчёта.")

    except (OSError, UnicodeError) as error:
        print(f"Не удалось прочитать файл: {error}")



def main():
    """Запускает главный цикл программы."""
    
    while True:
        show_menu()
        
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == "1":
            analyze_file()
        elif choice == "2":
            print("\nРабота программы завершена.")
            break
        else:
            print("\nОшибка: выберите пункт 1 или 2.")


if __name__ == "__main__":
    main()