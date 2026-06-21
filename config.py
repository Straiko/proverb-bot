import os
from dataclasses import dataclass


@dataclass
class Config:
    BOT_TOKEN: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    DB_PATH: str = "data/bot.db"
    PROVERBS_PATH: str = "data/proverbs.json"


def load_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN", ""),
        GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
    )
