from typing import Optional

from pydantic import BaseSettings, EmailStr

from app.core.constants import APP_DESCRIPTION, APP_TITLE, APP_URL


class Settings(BaseSettings):
    app_title: str = APP_TITLE
    app_description: str = APP_DESCRIPTION
    database_url: str = APP_URL
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
