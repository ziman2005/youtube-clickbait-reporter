import csv
import pytest
from utils import read_csv_files

def test_read_csv_single_file(tmp_path):
    """Чтение одного корректного CSV-файла."""
    file_path = tmp_path / "data.csv"
    content = [
        "title,ctr,retention_rate,views",
        "Video A,18.5,35,100",
        "Video B,22.0,28,200",
    ]
    file_path.write_text("\n".join(content), encoding="utf-8")

    result = read_csv_files([str(file_path)])

    expected = [
        {"title": "Video A", "ctr": 18.5, "retention_rate": 35.0},
        {"title": "Video B", "ctr": 22.0, "retention_rate": 28.0},
    ]
    assert result == expected


def test_read_csv_multiple_files(tmp_path):
    """Чтение нескольких файлов -> данные объединяются."""
    file1 = tmp_path / "data1.csv"
    file2 = tmp_path / "data2.csv"
    file1.write_text("title,ctr,retention_rate\nA,10.1,20.2\n", encoding="utf-8")
    file2.write_text("title,ctr,retention_rate\nB,30.3,40.4\n", encoding="utf-8")

    result = read_csv_files([str(file1), str(file2)])

    assert len(result) == 2
    assert result[0]["title"] == "A"
    assert result[1]["title"] == "B"


def test_read_csv_missing_file(tmp_path, capsys):
    """Отсутствующий файл: предупреждение, данные из существующих собираются."""
    good_file = tmp_path / "good.csv"
    good_file.write_text("title,ctr,retention_rate\nGood,99.9,10.0\n", encoding="utf-8")
    missing_file = tmp_path / "missing.csv"

    result = read_csv_files([str(missing_file), str(good_file)])

    assert len(result) == 1
    assert result[0]["title"] == "Good"

    captured = capsys.readouterr()
    assert "Ошибка: файл" in captured.out
    assert "missing.csv" in captured.out


def test_read_csv_invalid_numbers(tmp_path):
    """Строки с нечисловыми ctr/retention_rate пропускаются."""
    file_path = tmp_path / "data.csv"
    content = [
        "title,ctr,retention_rate",
        "Valid,20.0,30.0",
        "BadCTR,not_a_number,40.0",
        "BadRetention,25.0,invalid",
        "BothBad,abc,def",
    ]
    file_path.write_text("\n".join(content), encoding="utf-8")

    result = read_csv_files([str(file_path)])

    assert len(result) == 1
    assert result[0]["title"] == "Valid"


def test_read_csv_missing_columns(tmp_path, capsys):
    """Файл без обязательных колонок игнорируется (пропускается)."""
    file_path = tmp_path / "data.csv"
    file_path.write_text("title,ctr,views\nA,10,100\n", encoding="utf-8")

    result = read_csv_files([str(file_path)])

    assert result == []
    captured = capsys.readouterr()
    assert captured.out == ""


def test_read_csv_empty_file(tmp_path):
    """Пустой файл (только заголовок или без строк)."""
    file_path = tmp_path / "empty.csv"
    file_path.write_text("title,ctr,retention_rate\n", encoding="utf-8")

    result = read_csv_files([str(file_path)])
    assert result == []

    empty_file = tmp_path / "totally_empty.csv"
    empty_file.write_text("", encoding="utf-8")
    result2 = read_csv_files([str(empty_file)])
  
    assert result2 == []