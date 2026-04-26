from openai import AsyncOpenAI

from ton_mind_bot.config import settings


class OpenAIService:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def chat(self, prompt: str, premium: bool) -> tuple[str, str]:
        model = "gpt-4o" if premium else "gpt-4o-mini"
        response = await self.client.responses.create(
            model=model,
            input=[{"role": "system", "content": "You are TON blockchain analyst."}, {"role": "user", "content": prompt}],
        )
        return response.output_text, model
