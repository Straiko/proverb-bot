import re
import random
from typing import Optional

try:
    from groq import Groq
except ImportError:
    Groq = None


class AIMatcher:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        if Groq and api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = None
        self.model = model

    def _keyword_search(self, query: str, proverbs: list[dict]) -> list[dict]:
        query_lower = query.lower()
        words = set(re.findall(r'\w+', query_lower))

        scored = []
        for p in proverbs:
            text_lower = p["text"].lower()
            score = 0
            for w in words:
                if len(w) > 2 and w in text_lower:
                    score += 1
            if score > 0:
                scored.append((score, p))

        scored.sort(key=lambda x: -x[0])
        return [p for _, p in scored[:30]]

    def match_proverb(self, user_message: str, proverbs: list[dict]) -> str:
        if not proverbs:
            return "Извините, база пословиц пуста."

        candidates = self._keyword_search(user_message, proverbs)

        if not candidates:
            candidates = random.sample(proverbs, min(20, len(proverbs)))

        if not self.client:
            return random.choice(candidates)["text"]

        proverbs_text = "\n".join([f"{i+1}. {p['text']}" for i, p in enumerate(candidates)])

        prompt = f"""Подбери одну русскую пословицу или поговорку по запросу пользователя.

Запрос: {user_message}

Варианты:
{proverbs_text}

Выбери лучший вариант. Ответь ТОЛЬКО номером и текстом пословицы."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()

            for p in candidates:
                if p["text"] in answer:
                    return p["text"]

            return candidates[0]["text"]
        except Exception:
            return candidates[0]["text"]
