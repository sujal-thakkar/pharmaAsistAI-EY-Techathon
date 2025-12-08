"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings
from typing import List, Literal
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Provider Selection: "gemini" or "openai"
    llm_provider: Literal["gemini", "openai"] = "gemini"
    
    # API Keys
    gemini_api_key: str = ""
    openai_api_key: str = ""
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./pharmaassist.db"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # ChromaDB
    chroma_persist_directory: str = "./chroma_db"
    
    # PDF Storage
    pdf_directory: str = "./data/pdfs"
    
    # Agent Configuration
    max_agent_steps: int = 10
    agent_timeout: int = 120
    
    # Model Configuration
    gemini_model: str = "gemini-1.5-flash"
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "models/embedding-001"  # Gemini embedding model
    
    @property
    def llm_model(self) -> str:
        """Get the appropriate model based on provider."""
        if self.llm_provider == "gemini":
            return self.gemini_model
        return self.openai_model
    
    @property
    def active_api_key(self) -> str:
        """Get the API key for the active provider."""
        if self.llm_provider == "gemini":
            return self.gemini_api_key
        return self.openai_api_key
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
