import csv
from typing import List, Dict, Any

def read_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Читает CSV-файлы и возвращает список записей с полями:
    title, ctr (float), retention_rate (float).
    """
    all_data = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    continue
                required_fields = {'title', 'ctr', 'retention_rate'}
                if not required_fields.issubset(reader.fieldnames):
                    continue

                for row in reader:
                    try:
                        ctr_val = float(row['ctr'])
                        retention_val = float(row['retention_rate'])
                    except (ValueError, TypeError):
                        continue

                    all_data.append({
                        'title': row['title'],
                        'ctr': ctr_val,
                        'retention_rate': retention_val
                    })
        except FileNotFoundError:
            print(f"Ошибка: файл {file_path} не найден.")
            continue
        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")
            continue

    return all_data