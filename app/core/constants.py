APP_TITLE = 'QRKot'
APP_DESCRIPTION = 'Благотворительный фонд поддержки котиков'
APP_URL = 'sqlite+aiosqlite:///./fastapi.db'
MIN_LENGHT_PASSWORD = 3
USER_IS_REGISTERED = 'Пользователь {} зарегистрирован.'
WARNING_LENGHT_PASSWORD = 'Password should be at least 3 characters'
WARNING_PASSWORD_CONTAIN_EMAIL = 'Пароль не должен содержать e-mail'
WARNING_PROJECT_NOT_FOUND = 'Проект не найден!'
WARNING_PROJECT_NOT_EDIT = 'Закрытый проект нельзя редактировать!'
WARNING_PROJECT_NOT_DELETE = (
    'В проект были внесены средства, не подлежит удалению!'
)
WARNING_PROJECT_NAME_NOT_UNIQUE = 'Проект с таким именем уже существует!'
WARNING_PROJECT_INVEST = (
    'В проект были внесены средства, не подлежит удалению!'
)
WARNING_PROJECT_AMOUNT = (
    'Нелья установить значение full_amount меньше уже вложенной суммы.'
)
WARNING_USER_DELETE = 'Удаление пользователей запрещено!'
PROJECT_CREATE_EXAMPLES = {
    'project1': {
        'summary': 'Правильный запрос',
        'value': {
            'name': 'Хороший кот - здоровый кот!',
            'description': 'Средства на медицинское обслуживание',
            'full_amount': 200_000
        }
    },
    'project2': {
        'summary': 'Отсутствует обязательный параметр',
        'value': {
            'name': 'Всех по коммуналкам!',
            'full_amount': 100_000
        }
    },
    'project3': {
        'summary': 'Некорректная требуемая сумма пожертвований',
        'value': {
            'name': 'Счастливый кот - сытый кот!',
            'description': 'Средства на корм оставшимся без попечения кошкам',
            'full_amount': -500_000
        }
    }
}
PROJECT_UPDATE_EXAMPLES = {
    'project1': {
        'summary': 'Правильный запрос',
        'value': {
            'name': 'Хороший кот - мертвый кот!',
            'description': 'Средства на медицинское обслуживание',
            'full_amount': 300_000
        }
    },
    'project2': {
        'summary': 'Имя проекта уже есть в БД',
        'value': {
            'name': 'Хороший кот - здоровый кот!',
            'description': 'Средства на лечение',
            'full_amount': 400_000
        }
    },
    'project3': {
        'summary': 'Уменьшение суммы пожертвований',
        'value': {
            'description': 'Средства на корм оставшимся без попечения кошкам',
            'full_amount': 50_000
        }
    }
}
DONATION_CREATE_EXAMPLES = {
    'donation1': {
        'summary': 'Правильный запрос',
        'value': {
            'full_amount': 50,
            'comment': 'Пожертвования от мецената',
        }
    },
    'donation2': {
        'summary': 'Отсутствует обязательный параметр',
        'value': {
            'comment': 'Пожертвования от любителя котов',
        }
    },
    'donation3': {
        'summary': 'Некорректная сумма пожертвования',
        'value': {
            'full_amount': -100_000,
            'comment': 'Очень не люблю кошек',
        }
    }
}
DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
GOOGLE_API_NAME_SHEETS = 'sheets'
GOOGLE_API_VERSION_SHEETS = 'v4'
GOOGLE_API_NAME_DRIVE = 'drive'
GOOGLE_API_VERSION_DRIVE = 'v3'
SPREADSHEET_TITLE = 'Отчёт от'
LOCATION_FORMAT = 'ru_RU'
SHEET_TYPE = 'GRID'
SHEET_ID = 0
SHEET_TITLE = 'Лист1'
SHEET_ROWS = 100
SHEET_COLUMNS = 11
PERMISSION_TYPE = 'user'
PERMISSION_ROLE = 'writer'
TITLE_NAME = 'Топ проектов по скорости закрытия'
PROJECT_NAME = 'Название проекта'
PROJECT_DURATION = 'Время сбора'
PROJECT_DESCRIPTION = 'Описание'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/{}'
SPREADSHEET_BODY = {
    'properties': {
        'title': SPREADSHEET_TITLE,
        'locale': LOCATION_FORMAT
    },
    'sheets': [{
        'properties': {
            'sheetType': SHEET_TYPE,
            'sheetId': SHEET_ID,
            'title': SHEET_TITLE,
            'gridProperties': {
                'rowCount': SHEET_ROWS,
                'columnCount': SHEET_COLUMNS
            }
        }
    }]
}
PERMISSION_BODY = {
    'type': PERMISSION_TYPE,
    'role': PERMISSION_ROLE,
}
TABLE_VALUES = [
    [SPREADSHEET_TITLE],
    [TITLE_NAME],
    [PROJECT_NAME, PROJECT_DURATION, PROJECT_DESCRIPTION]
]
