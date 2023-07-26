from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


COLUMN_COUNT = 11
FORMAT = "%Y/%m/%d %H:%M:%S"
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
LOCALE = 'ru_RU'
ROW_COUNT = 100
SHEET_ID = 0
SHEET_TITLE = 'Лист1'
TITLE = f'Отчет на {NOW_DATE_TIME}'
TABLE_VALUES = [
    ['Отчет от', NOW_DATE_TIME],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': TITLE,
                       'locale': LOCALE},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': SHEET_ID,
                                   'title': SHEET_TITLE,
                                   'gridProperties': {
                                       'rowCount': ROW_COUNT,
                                       'columnCount': COLUMN_COUNT
                                   }}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_VALUES
    for project in projects:
        new_row = [
            str(project['name']),
            str(project['duration']),
            str(project['description']),
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
