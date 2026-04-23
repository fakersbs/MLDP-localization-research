"""Configuration management for the application"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = "MLDP Localization Research Assistant"
    api_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False") == "True"
    
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://mldp_user:mldp_password@localhost:5432/mldp_research"
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "False") == "True"
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # PubMed Configuration
    pubmed_api_key: str = os.getenv("PUBMED_API_KEY", "")
    pubmed_email: str = os.getenv("PUBMED_EMAIL", "")
    
    # NCBI Configuration
    ncbi_api_key: str = os.getenv("NCBI_API_KEY", "")
    
    # Server Configuration
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    server_reload: bool = os.getenv("SERVER_RELOAD", "True") == "True"
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
