from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra

from app.core.constants import DONATION_CREATE_EXAMPLES


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'examples': DONATION_CREATE_EXAMPLES
        }


class DonationShortDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationShortDB):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
