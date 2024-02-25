from datetime import datetime
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import InvestModel


async def close_obj(
    obj_list: list[InvestModel],
    session: AsyncSession
) -> None:
    for obj in obj_list:
        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()
            session.add(obj)


async def append_money(
    objects: list[InvestModel],
    obj_for_invest: InvestModel,
    session: AsyncSession
) -> None:
    for obj_from_invest in objects:
        money_for_append = min(
            obj_for_invest.full_amount - obj_for_invest.invested_amount,
            obj_from_invest.full_amount - obj_from_invest.invested_amount
        )
        obj_from_invest.invested_amount += money_for_append
        obj_for_invest.invested_amount += money_for_append
        await close_obj([obj_from_invest, obj_for_invest], session)


async def investment(
    obj_for_invest: InvestModel,
    model: Type[InvestModel],
    session: AsyncSession
) -> InvestModel:
    objects = await session.scalars(
        select(model).where(model.fully_invested == 0).order_by(
            model.create_date)
    )
    await append_money(objects.all(), obj_for_invest, session)
    await session.commit()
    await session.refresh(obj_for_invest)
    return obj_for_invest
