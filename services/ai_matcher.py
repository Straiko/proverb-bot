import re
import random

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

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = text.replace('ё', 'е')
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def _search(self, query: str, proverbs: list[dict]) -> list[dict]:
        query_norm = self._normalize(query)
        query_words = [w for w in re.findall(r'\w+', query_norm) if len(w) > 2]

        scored = []
        for p in proverbs:
            text_norm = self._normalize(p["text"])

            # Exact phrase match
            if query_norm in text_norm:
                scored.append((1000, p))
                continue

            # Word matches
            matches = 0
            for w in query_words:
                if re.search(r'\b' + re.escape(w) + r'\w*\b', text_norm):
                    matches += 1

            if matches > 0:
                score = matches * 30 + (matches / max(len(query_words), 1)) * 50
                scored.append((score, p))

        scored.sort(key=lambda x: -x[0])
        return [p for _, p in scored[:20]]

    def match_proverb(self, user_message: str, proverbs: list[dict]) -> str:
        if not proverbs:
            return "Извините, база пословиц пуста."

        candidates = self._search(user_message, proverbs)

        if not candidates:
            return "Не нашлось подходящей пословицы. Попробуйте перефразировать."

        if not self.client or len(candidates) <= 1:
            return candidates[0]["text"]

        proverbs_text = "\n".join([f"{i+1}. {p['text']}" for i, p in enumerate(candidates[:10])])

        prompt = f"""Запрос: "{user_message}"

Выбери лучшую пословицу:
{proverbs_text}

Ответь ТОЛЬКО номером."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.1
            )
            answer = response.choices[0].message.content.strip()
            num = int(re.search(r'\d+', answer).group()) - 1
            if 0 <= num < len(candidates):
                return candidates[num]["text"]
            return candidates[0]["text"]
        except Exception:
            return candidates[0]["text"]
