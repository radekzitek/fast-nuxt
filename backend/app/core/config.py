"""
Application Configuration Management.

This module defines the application settings using Pydantic's BaseSettings.
It allows for loading configuration from environment variables and a .env file.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        SQLALCHEMY_DATABASE_URL (str): The database connection URL.
                                       Defaults to a local SQLite database file.
    """
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./data/fast-nuxt.db"  # Default to a local SQLite file

    class Config:
        """
        Pydantic configuration class for Settings.

        Attributes:
            env_file (str): The name of the environment file to load settings from.
        """
        env_file = ".env"


settings = Settings()
"""
Global instance of the application settings.
This instance is used throughout the application to access configuration values.
"""
