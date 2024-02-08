from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """This automatically loads our env file for us and validates the type of data,
     no need for CAPS """
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


    class Config:
        """Very important"""
        env_file = ".env"

settings = Settings()
print(settings.db_username, "username")


