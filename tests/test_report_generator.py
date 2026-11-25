import json
from report_generator import (
    generate_txt_report,
    generate_json_report,
)


def test_generate_txt_report(tmp_path):
    """Проверка формирования текстового отчёта."""
    
    statistics = {
        "total": 5,
        "levels": {
            "INFO": 1,
            "WARNING": 1,
            "ERROR": 2,
            "CRITICAL": 1,
        },
        "errors": 3,
        "warnings": 1,
    }

    top_errors = [
        ("Database error", 2),
        ("Server unavailable", 1),
    ]

    output_path = tmp_path / "report.txt"

    generate_txt_report(
        statistics,
        top_errors,
        1,
        str(output_path),
    )

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "Всего записей: 5" in content
    assert "Количество ошибок: 3" in content
    assert "Некорректных строк: 1" in content
    assert "Database error" in content


def test_generate_json_report(tmp_path):
    """Проверка формирования JSON-отчёта."""

    statistics = {
        "total": 5,
        "levels": {"INFO": 1, "ERROR": 4},
        "errors": 4,
        "warnings": 0,
    }

    top_errors = [
        ("Database error", 3),
    ]

    output_path = tmp_path / "report.json"

    generate_json_report(
        statistics,
        top_errors,
        2,
        str(output_path),
    )

    assert output_path.exists()

    with output_path.open(encoding="utf-8") as file:
        data = json.load(file)

    assert data["statistics"]["total"] == 5
    assert data["statistics"]["errors"] == 4
    assert data["invalid_lines_count"] == 2
    assert data["top_errors"][0]["message"] == "Database error"
    assert data["top_errors"][0]["count"] == 3
