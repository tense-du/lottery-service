from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import field_validator
import os


class Settings(BaseSettings):
    """Application settings and configuration.

    This class defines all configuration settings for the application.
    Settings are loaded from environment variables or a .env file.

    Attributes:
        DATABASE_URL (str): PostgreSQL database connection URL
        LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD (int): Maximum number of days in the future
            for which participants can submit ballots. Must be greater than 0.
        CELERY_BROKER_URL (str): Redis URL for Celery message broker
        CELERY_RESULT_BACKEND (str): Redis URL for Celery result backend
        REDIS_PASSWORD (Optional[str]): Redis password if authentication is enabled
        ENCRYPTION_KEY (str): Key used for encrypting sensitive data
        HASH_SALT (str): Salt for hashing sensitive data (for searching)
        CELERY_DEFAULT_QUEUE (str): Required queue name for Celery tasks
    """
    DATABASE_URL: str
    # Setting to allow participant to register to lotteries up to N days ahead
    LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD: int
    REDIS_PASSWORD: Optional[str] = None
    ENCRYPTION_KEY: str
    HASH_SALT: str
    CELERY_DEFAULT_QUEUE: str  # Required queue name for Celery tasks

    @field_validator("LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD")
    @classmethod
    def validate_lottery_draw_date_max_days_ahead(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD must be greater than 0")
        return v

    @property
    def CELERY_BROKER_URL(self) -> str:
        host = "localhost" if os.getenv("ENV_MODE") != "docker" else "redis"
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{host}:6379/0"
        return f"redis://{host}:6379/0"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        host = "localhost" if os.getenv("ENV_MODE") != "docker" else "redis"
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{host}:6379/0"
        return f"redis://{host}:6379/0"

    class Config:
        """Pydantic settings configuration.

        Attributes:
            env_file (str): Path to the .env file
            env_file_encoding (str): Encoding of the .env file
            extra (str): How to handle extra fields in the environment
        """
        # Get the environment mode from ENV_MODE, default to 'local'
        env_mode = os.getenv("ENV_MODE", "local")
        env_file = f".env.{env_mode}" if env_mode != "local" else ".env"
        env_file_encoding = "utf-8"
        # Allow extra fields in the environment
        extra = "allow"


# Create a singleton instance that can be imported
settings = Settings()
