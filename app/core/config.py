from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pokie Dokie"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username="postgres",
            password="postgres",
            host="localhost",
            port=5432,
            path="/pokie_dokie",
        )
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 