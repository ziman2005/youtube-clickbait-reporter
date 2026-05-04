import argparse
import sys
from typing import List, Dict, Any

from utils import read_csv_files

from reports.clickbait import generate_clickbait_report

AVAILABLE_REPORTS = {
    'clickbait': generate_clickbait_report,
    # будущие отчёты добавляются сюда
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Анализ метрик YouTube-видео и формирование отчётов'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV-файлам с данными (можно указать несколько)'
    )
    parser.add_argument(
        '--report',
        required=True,
        help=f'Название отчёта. Доступны: {", ".join(AVAILABLE_REPORTS.keys())}'
    )
    args = parser.parse_args()

    try:
        data = read_csv_files(args.files)
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}", file=sys.stderr)
        sys.exit(1)

    if not data:
        print("Нет данных для обработки. Проверьте файлы.", file=sys.stderr)
        sys.exit(0)

    report_name = args.report.lower()
    if report_name not in AVAILABLE_REPORTS:
        print(
            f"Неизвестный отчёт: {args.report}. "
            f"Доступны: {', '.join(AVAILABLE_REPORTS.keys())}",
            file=sys.stderr
        )
        sys.exit(1)

    report_func = AVAILABLE_REPORTS[report_name]

    try:
        output = report_func(data)
    except Exception as e:
        print(f"Ошибка при формировании отчёта: {e}", file=sys.stderr)
        sys.exit(1)

    print(output)


if __name__ == '__main__':
    main()