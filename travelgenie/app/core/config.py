from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    WEATHER_API_KEY: str

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    model_config = {
        "env_file": ".env"
    }


settings = Settings()