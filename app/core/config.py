from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class Environment(int, Enum):
    dev = 1
    test = 2
    prod = 3

class Settings(BaseSettings):
    app_name: str = "EMS system"
    debug: bool = False
    db_url: str
    jwt_secret: str
    jwt_expiry: int
    environment: Environment = Environment.dev

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()