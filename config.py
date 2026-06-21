import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class Config:
    BOT_TOKEN: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    DB_PATH: str = str(BASE_DIR / "data" / "bot.db")
    PROVERBS_PATH: str = str(BASE_DIR / "data" / "proverbs.json")


def load_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN", ""),
        GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
    )
