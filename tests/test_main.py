
from main import main


def test_main_exit(monkeypatch, capsys):
    """Проверяет выход из программы через главное меню."""

    # Имитируем ввод пользователя: сначала выбираем выход
    inputs = iter(["2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    # Получаем текст, который вывела программа
    captured = capsys.readouterr()

    assert "Работа программы завершена." in captured.out


def test_main_invalid_choice(monkeypatch, capsys):
    """Проверяет обработку неправильного пункта меню."""

    # Сначала вводим неправильный пункт, затем выходим
    inputs = iter(["5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()

    assert "Ошибка: выберите пункт 1 или 2." in captured.out
    assert "Работа программы завершена." in captured.out


from main import analyze_file


def test_analyze_file_missing_path(monkeypatch, capsys, tmp_path):
    """Проверяет обработку несуществующего файла."""

    missing_file = tmp_path / "missing.log"

    monkeypatch.setattr(
        "builtins.input",
        lambda _: str(missing_file)
    )

    analyze_file()

    captured = capsys.readouterr()

    assert "Ошибка: указанный файл не найден." in captured.out


def test_analyze_file_without_report(monkeypatch, capsys, tmp_path):
    """Проверяет анализ файла без сохранения отчёта."""

    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-11-20 10:15:32 INFO Application started\n"
        "2026-11-20 10:16:01 ERROR Database connection failed\n"
        "2026-11-20 10:17:45 WARNING High memory usage\n",
        encoding="utf-8"
    )

    inputs = iter([str(log_file), "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    analyze_file()

    captured = capsys.readouterr()

    assert "Всего записей: 3" in captured.out
    assert "Ошибок: 1" in captured.out
    assert "Предупреждений: 1" in captured.out
    assert "Отчёт не сохранялся." in captured.out