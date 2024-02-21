from pydantic_settings import BaseSettings
from pydantic import Field
# from .setup_a import ENVIRONMENT


class Settings(BaseSettings):
    """This automatically loads our env file for us and validates the type of data,
     no need for CAPS """
    # Allow both local and Docker environment variable names
    postgres_user: str 
    postgres_password: str 
    postgres_host: str
    postgres_port: str
    postgres_db: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """Very important"""
        env_file = ".env.local" # ".env.dev"
        extra = 'ignore'

settings = Settings()
# print(settings.db_username, "username")


