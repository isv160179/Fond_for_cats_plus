from typing import Union, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Boolean, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import GetAllCreateBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectUpdate, CharityProjectCreate,
)


class CRUDCharityProject(
    GetAllCreateBase[CharityProject, CharityProjectCreate]
):

    @staticmethod
    async def update(
        project_db: CharityProject,
        project_json: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        project_from_db_dict = jsonable_encoder(project_db)
        project_from_json_dict = project_json.dict(exclude_unset=True)
        for field in project_from_db_dict:
            if field in project_from_json_dict:
                setattr(project_db, field, project_from_json_dict[field])
        session.add(project_db)
        await session.commit()
        await session.refresh(project_db)
        return project_db

    @staticmethod
    async def delete(
        project_db: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(project_db)
        await session.commit()
        return project_db

    @staticmethod
    async def check_unique_name(
        field_name: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        exists_criteria = (
            select(CharityProject).where(
                CharityProject.name == field_name
            ).exists()
        )
        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()

    @staticmethod
    async def get_project_by_id(
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        return await session.get(CharityProject, project_id)

    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession,
    ) -> list[CharityProject]:
        projects = await session.scalars(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                func.julianday(CharityProject.close_date) - func.julianday(
                    CharityProject.create_date
                )
            )
        )
        return projects.all()


project_crud = CRUDCharityProject(CharityProject)
