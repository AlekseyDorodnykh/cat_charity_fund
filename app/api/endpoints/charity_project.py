from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_before_delete,
    check_before_update,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import allocate_donations

router = APIRouter()

ALL_PROJECTS = "Список всех проектов"
CREATE_PROJECT = "Создать проект"
DELETE_PROJECT = "Удалить проект"
UPDATE_PROJECT = "Редактировать проект"


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=CREATE_PROJECT,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создает благотворительный проект. Только для суперюзеров!"""
    await check_name_duplicate(
        charity_project.name, session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session, commit=False
    )
    session.add_all(
        allocate_donations(
            target=new_charity_project,
            sources=await donation_crud.get_not_closed(session),
        )
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary=ALL_PROJECTS,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Просмотр списка всех благотворительных проектов."""
    return await charity_project_crud.get_all(session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary=DELETE_PROJECT,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Удаляет благотворительный проект. Только для суперюзеров."""
    charity_project = await check_before_delete(
        project_id, session
    )
    return await charity_project_crud.remove(
        charity_project, session
    )


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary=UPDATE_PROJECT,
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Редактирует благотворительный проект. Только для суперюзеров."""
    charity_project_db = await check_before_update(
        project_id, charity_project_in, session
    )
    return await charity_project_crud.update(
        charity_project_db, session, charity_project_in
    )
