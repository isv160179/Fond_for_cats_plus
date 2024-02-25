from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_invest_amount,
    check_full_amount,
    check_project_exist_not_close
)
from app.core.constants import (
    WARNING_PROJECT_NOT_DELETE,
    WARNING_PROJECT_NOT_EDIT
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.models import Donation
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.donations import investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    new_project_json: Annotated[CharityProjectCreate, Body(
        examples=CharityProjectCreate.Config.schema_extra['examples']
    )],
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """
    Только для суперюзеров.

    Создаёт благотворительный проект.
    """
    await check_name_duplicate(new_project_json.name, session)
    new_project_db = await project_crud.create(new_project_json, session)
    return await investment(new_project_db, Donation, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await project_crud.get_all(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project_json: Annotated[CharityProjectUpdate, Body(
        examples=CharityProjectUpdate.Config.schema_extra['examples']
    )],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project_db = await check_project_exist_not_close(
        project_id,
        WARNING_PROJECT_NOT_EDIT,
        session
    )
    if project_json.full_amount is not None:
        check_full_amount(project_db, project_json.full_amount)
    if project_json.name is not None:
        await check_name_duplicate(project_json.name, session)
    return await project_crud.update(project_db, project_json, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    project_db = await check_project_exist_not_close(
        project_id,
        WARNING_PROJECT_NOT_DELETE,
        session
    )
    check_invest_amount(project_db)
    project_db = await project_crud.delete(project_db, session)
    return project_db
