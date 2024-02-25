from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import Donation, User, CharityProject
from app.schemas.donation import DonationDB, DonationCreate, DonationShortDB
from app.services.donations import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_all(session)


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True,
)
async def create_donation(
    new_donation_json: Annotated[DonationCreate, Body(
        examples=DonationCreate.Config.schema_extra['examples']
    )],
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    """
    Сделать пожертвование.
    """
    new_donation_db = await donation_crud.create(
        new_donation_json,
        session,
        user
    )
    return await investment(new_donation_db, CharityProject, session)


@router.get(
    '/my', response_model=list[DonationShortDB],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Вернуть список пожертвований пользователя, выполняющего запрос.
    """
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
