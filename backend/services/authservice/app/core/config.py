from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #App
    app_name: str = "FastAuth"
    debug: bool = True
    cookie_secure: bool = False
    cors_origins: list = ["*"]
    retry_statuses: list = [500, 501, 502, 503, 504]
    notify_max_retries: int = 5
    notify_service_url: str = "http://127.0.0.1:7070/api/"
    
    # Database
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str
    test_db_name: str
    
    # JWT
    secret: str
    access_cookie_name: str
    refresh_cookie_name: str
    token_location: str
    algorithm: str
    access_token_expire_minutes: int = Field(default=60, gt=0)
    refresh_token_expire_days: int = Field(default=30, gt=0)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def get_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def get_test_database_url(self) ->str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.test_db_name}"
        
settings = Settings()