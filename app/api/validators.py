from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    WARNING_PROJECT_NOT_FOUND,
    WARNING_PROJECT_NAME_NOT_UNIQUE,
    WARNING_PROJECT_INVEST,
    WARNING_PROJECT_AMOUNT,
)
from app.crud.charity_project import project_crud
from app.models import CharityProject


async def check_project_exist_not_close(
    project_id: int,
    message: str,
    session: AsyncSession
) -> CharityProject:
    project_db = await project_crud.get_project_by_id(project_id, session)
    if project_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=WARNING_PROJECT_NOT_FOUND
        )
    if project_db.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return project_db


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    if await project_crud.check_unique_name(project_name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=WARNING_PROJECT_NAME_NOT_UNIQUE,
        )


def check_invest_amount(
    project_db: CharityProject,
) -> None:
    if project_db.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=WARNING_PROJECT_INVEST,
        )


def check_full_amount(
    project_db: CharityProject,
    full_amount: int,
) -> None:
    if full_amount < project_db.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=WARNING_PROJECT_AMOUNT,
        )
