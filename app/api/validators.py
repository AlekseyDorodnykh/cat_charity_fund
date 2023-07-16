from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


ALREADY_INVESTED_ERROR = 'В проект были внесены средства, не подлежит удалению!'
CLOSED_PROJECT_ERROR = 'Закрытый проект нельзя редактировать!'
DECREASE_INVESTMENT_ERROR = 'Нельзя установить сумму меньше уже вложенной.'
NAME_DUPLICATED = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект с id {id} не найден!'


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name, session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=400, detail=NAME_DUPLICATED,
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка наличия проекта в базе."""
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_NOT_FOUND.format(id=charity_project_id)
        )
    return charity_project


async def check_before_delete(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверка на наличие вложенных средств перед удалением."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400, detail=ALREADY_INVESTED_ERROR
        )
    return charity_project


async def check_before_update(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    """Проверка перед обновлением на наличие вложенных средств и закрытый"""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=400, detail=CLOSED_PROJECT_ERROR
        )
    full_amount_update = charity_project_in.full_amount
    if (
        full_amount_update and
        charity_project.invested_amount > full_amount_update
    ):
        raise HTTPException(
            status_code=422, detail=DECREASE_INVESTMENT_ERROR,
        )
    await check_name_duplicate(
        charity_project_in.name, session
    )
    return charity_project
