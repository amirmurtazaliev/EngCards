from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "EngCards CardService"
    debug: bool = True

    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_pass: str = "1234"

    secret: str = "SECRET_KEY"
    algorithm: str = "HS256"
    access_cookie_name: str = "my_access_token"
    cards_schema: str = "cards"
    access_token_expire_minutes: int = Field(default=60, gt=0)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()