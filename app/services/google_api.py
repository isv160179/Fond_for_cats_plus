from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    DATETIME_FORMAT,
    SPREADSHEET_TITLE,
    LOCATION_FORMAT,
    SHEET_TYPE,
    SHEET_ID,
    SHEET_TITLE,
    SHEET_ROWS,
    SHEET_COLUMNS,
    GOOGLE_API_NAME_SHEETS,
    GOOGLE_API_VERSION_SHEETS,
    GOOGLE_API_NAME_DRIVE,
    GOOGLE_API_VERSION_DRIVE,
    PERMISSION_ROLE,
    PERMISSION_TYPE,
    TITLE_NAME,
    PROJECT_NAME,
    PROJECT_DURATION,
    PROJECT_DESCRIPTION
)
from app.models import CharityProject


async def spreadsheets_create(
    wrapper_services: Aiogoogle
) -> str:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover(
        GOOGLE_API_NAME_SHEETS,
        GOOGLE_API_VERSION_SHEETS

    )
    spreadsheet_body = {
        'properties': {
            'title': SPREADSHEET_TITLE + now_date_time,
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
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': PERMISSION_TYPE,
                        'role': PERMISSION_ROLE,
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(
        GOOGLE_API_NAME_DRIVE,
        GOOGLE_API_VERSION_DRIVE
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    charity_projects: list[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover(
        GOOGLE_API_NAME_SHEETS,
        GOOGLE_API_VERSION_SHEETS
    )
    table_values = [
        [SPREADSHEET_TITLE, now_date_time],
        [TITLE_NAME],
        [PROJECT_NAME, PROJECT_DURATION, PROJECT_DESCRIPTION]
    ]
    for project in charity_projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ]
        if len(new_row) <= SHEET_ROWS:
            table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{SHEET_ROWS}C{SHEET_COLUMNS}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
