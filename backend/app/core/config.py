import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./data/fast-nuxt.db" # Default to a local SQLite file

    class Config:
        env_file = ".env"

settings = Settings()