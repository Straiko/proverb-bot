import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


@dataclass
class Config:
    BOT_TOKEN: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    DB_PATH: str = str(DATA_DIR / "bot.db")
    PROVERBS_PATH: str = str(DATA_DIR / "proverbs.json")


def load_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN", ""),
        GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
    )
