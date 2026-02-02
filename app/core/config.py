from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_URL: str
    DATABASE_URL: str
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()