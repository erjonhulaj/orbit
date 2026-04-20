import os
from dotenv import load_dotenv

# Load all variables from .env into the environment
load_dotenv()

class Config:
    """Central configuration loader. Every module pulls from here, never from .env."""

    # GitHub credentials loaded from environment
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USERNAME: str = os.getenv("GITHUB_USERNAME", "")

    @classmethod
    def validate(cls) -> None:
        """Raise early if required config values are missing."""
        if not cls.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is missing from .env.")
        if not cls.GITHUB_USERNAME:
            raise ValueError("GITHUB_USERNAME is missing from .env.")