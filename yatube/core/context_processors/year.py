from datetime import datetime


def year(request):
    current_date = datetime.now()
    current_year = current_date.strftime('%Y')
    """Добавляет переменную с текущим годом."""
    return {
        'year': int(current_year)
    }
