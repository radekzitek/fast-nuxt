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
    SQLALCHEMY_DATABASE_URL: str = "postgresql://fastnuxt:fastnuxtpass@localhost:5432/fastnuxtdb"  # Default to local PostgreSQL
    OPENAI_API_KEY: str  # Add this line to allow loading the OpenAI API key from .env
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def database_url(self) -> str:
        # Always use the hardcoded PostgreSQL URL
        return self.SQLALCHEMY_DATABASE_URL

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

print("Loaded settings:")
for field, value in settings.model_dump().items():
    print(f"{field}: {value}")

# For convenience, expose the database URL as settings.database_url
