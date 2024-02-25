from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import GetAllCreateBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(
    GetAllCreateBase[Donation, DonationCreate]
):
    @staticmethod
    async def get_by_user(
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        donations = await session.scalars(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.all()


donation_crud = CRUDDonation(Donation)
