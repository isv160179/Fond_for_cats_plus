from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    DATETIME_FORMAT,
    SHEET_ROWS,
    SHEET_COLUMNS,
    GOOGLE_API_NAME_SHEETS,
    GOOGLE_API_VERSION_SHEETS,
    GOOGLE_API_NAME_DRIVE,
    GOOGLE_API_VERSION_DRIVE,
    SPREADSHEET_BODY,
    PERMISSION_BODY,
    TABLE_VALUES
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
    SPREADSHEET_BODY['properties']['title'] += now_date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(
        GOOGLE_API_NAME_DRIVE,
        GOOGLE_API_VERSION_DRIVE
    )
    PERMISSION_BODY['emailAddress'] = settings.email
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSION_BODY,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_projects: list[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover(
        GOOGLE_API_NAME_SHEETS,
        GOOGLE_API_VERSION_SHEETS
    )
    TABLE_VALUES[0].append(now_date_time)

    for project in charity_projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ]
        if len(new_row) <= SHEET_ROWS:
            TABLE_VALUES.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': TABLE_VALUES
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{SHEET_ROWS}C{SHEET_COLUMNS}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
