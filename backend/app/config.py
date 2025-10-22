from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase Configuration
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # Openrouter Configuration
    openrouter_api_key: str
    openrouter_model: str = "z-ai/glm-4.5-air:free"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: str = "http://localhost:3000"
    
    # Encryption
    encryption_key: str
    
    # LinkedIn OAuth (optional)
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    
    # Email Configuration (optional)
    sendgrid_api_key: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@creatorpulse.com"
    from_name: str = "CreatorPulse"
    
    # Advanced Auto-Newsletter API Keys (optional)
    firecrawl_api_key: str = ""
    google_trends_api_key: str = ""
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

