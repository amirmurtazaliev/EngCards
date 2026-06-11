from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    app_name: str = "Notification Service"
    cors_origins: list = ["*"]
    
    # Notification
    smtp_host: str = Field(env="SMTP_HOST")
    smtp_port: int = Field(env="SMTP_PORT")
    smtp_user: str = Field(env="SMTP_USER")
    smtp_password: str = Field(env="SMTP_PASSWORD")
    
    class Config:
        env_file = ".env"
    
settings = Settings()