import json
from groq import Groq


class AIMatcher:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self.client = Groq(api_key=api_key)
        self.model = model

    def match_proverb(self, user_message: str, proverbs: list[dict]) -> str:
        if not proverbs:
            return "Извините, база пословиц пуста."

        proverbs_text = "\n".join([f"- {p['text']}" for p in proverbs])

        prompt = f"""Ты помощник, который подбирает русские пословицы и поговорки.

Вопрос пользователя: {user_message}

Доступные пословицы:
{proverbs_text}

Выбери одну подходящую пословицу из списка выше, которая лучше всего отвечает на вопрос пользователя.
Ответь ТОЛЬКО текстом пословицы без объяснений, кавычков и дополнительного текста."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            import random
            return random.choice(proverbs)["text"]
