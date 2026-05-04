from tabulate import tabulate
from typing import List, Dict, Any

def generate_clickbait_report(data: List[Dict[str, Any]]) -> str:
    """
    Формирует отчёт о кликбейтных видео:
    - ctr > 15
    - retention_rate < 40
    Сортировка по убыванию ctr.
    Возвращает строку с таблицей для печати.
    """

    filtered = [
        item for item in data
        if item['ctr'] > 15 and item['retention_rate'] < 40
    ]
    
    filtered.sort(key=lambda x: x['ctr'], reverse=True)
    
    table_data = [
        [item['title'], item['ctr'], item['retention_rate']]
        for item in filtered
    ]
    headers = ['title', 'ctr', 'retention_rate']
    

    return tabulate(table_data, headers=headers, tablefmt='grid')