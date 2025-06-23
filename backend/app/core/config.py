from pydantic_settings import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "RFP Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-use-env-file"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "budget_calculator"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # OpenAI API
    OPENAI_API_KEY: Optional[str] = None  # Set to None to use free mock analysis
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 4096
    OPENAI_TEMPERATURE: float = 0.3
    
    # Google Gemini API (FREE!)
    GOOGLE_API_KEY: Optional[str] = "AIzaSyCsmPyvSuQxhV01O46dCbgjFe9rfMp_wQQ"
    
    # Hugging Face API (FREE Alternative!)
    HUGGINGFACE_API_KEY: Optional[str] = "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"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

settings = Settings() 