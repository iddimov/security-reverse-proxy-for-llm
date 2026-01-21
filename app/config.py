import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    """Centralized configuration for environment variables."""
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration at startup."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        if not cls.GEMINI_MODEL:
            raise ValueError("GEMINI_MODEL not found in environment")
