import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Admin IDs
    ADMIN_IDS: list[int] = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            self.ADMIN_IDS = [int(id_str.strip()) for id_str in admin_ids_str.split(",") if id_str.strip()]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./imam_malik.db")
    
    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Webhook URL for production
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")

    class Config:
        env_file = ".env"

settings = Settings()
