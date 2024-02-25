from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field, PositiveInt, validator, Extra

from app.core.constants import PROJECT_CREATE_EXAMPLES, PROJECT_UPDATE_EXAMPLES


class CharityProjectBase(BaseModel):
    name: Annotated[Optional[str], Field(min_length=1, max_length=100)] = None
    description: Annotated[Optional[str], Field(min_length=1)] = None
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(min_length=1)]
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'examples': PROJECT_CREATE_EXAMPLES
        }


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    class Config:
        schema_extra = {
            'examples': PROJECT_UPDATE_EXAMPLES
        }


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
