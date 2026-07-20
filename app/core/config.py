from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class Environment(str, Enum):
    DEV = "DEV"
    TEST = "TEST"
    PROD = "PROD"

class Settings(BaseSettings):
    app_name: str = "EMS system"
    debug: bool = False
    db_url: str
    jwt_secret: str
    jwt_expiry: int
    environment: Environment = Environment.DEV

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()