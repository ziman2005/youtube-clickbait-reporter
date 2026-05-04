import pytest
from reports.clickbait import generate_clickbait_report


def test_generate_clickbait_report_filters_and_sorts():
    """Проверка фильтрации (ctr>15, retention<40) и сортировки по убыванию ctr."""
    data = [
        {"title": "Low CTR", "ctr": 10.0, "retention_rate": 30.0},
        {"title": "High Retention", "ctr": 20.0, "retention_rate": 50.0},
        {"title": "Good 1", "ctr": 25.0, "retention_rate": 35.0},
        {"title": "Good 2", "ctr": 18.0, "retention_rate": 38.0},
        {"title": "Good 3", "ctr": 22.0, "retention_rate": 25.0},
    ]
    result = generate_clickbait_report(data)

    assert "Good 1" in result
    assert "Good 2" in result
    assert "Good 3" in result
    assert "Low CTR" not in result
    assert "High Retention" not in result

    idx1 = result.find("Good 1")
    idx3 = result.find("Good 3")
    idx2 = result.find("Good 2")
    assert idx1 < idx3 < idx2


def test_generate_clickbait_report_empty_data():
    """Пустой входной список -> таблица только с заголовками."""
    result = generate_clickbait_report([])
    assert "title" in result
    assert "ctr" in result
    assert "retention_rate" in result

    lines = result.splitlines()

    data_rows = [
        line
        for line in lines
        if "│" in line and "title" not in line and "ctr" not in line
    ]
    assert len(data_rows) == 0


def test_generate_clickbait_report_no_match():
    """Все видео не проходят фильтр -> пустая таблица."""
    data = [
        {"title": "Low CTR", "ctr": 10.0, "retention_rate": 30.0},
        {"title": "High Retention", "ctr": 20.0, "retention_rate": 60.0},
    ]
    result = generate_clickbait_report(data)
    assert "Low CTR" not in result
    assert "High Retention" not in result

    lines = result.splitlines()
    data_rows = [
        line
        for line in lines
        if "│" in line and "title" not in line and "ctr" not in line
    ]
    assert len(data_rows) == 0


def test_generate_clickbait_report_preserves_types():
    """Числовые значения остаются числами (на выводе могут быть как целые/дробные)."""
    data = [
        {"title": "Test", "ctr": 15.1, "retention_rate": 39.9},
    ]
    result = generate_clickbait_report(data)

    assert "15.1" in result
    assert "39.9" in result
