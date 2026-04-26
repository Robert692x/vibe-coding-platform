from openai import AsyncOpenAI

from ton_mind_bot.ai.system_prompt import FEW_SHOT, KNOWLEDGE_BLOCK, SYSTEM_PROMPT
from ton_mind_bot.config import settings


class OpenAIService:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def chat(self, prompt: str, premium: bool | None = None) -> tuple[str, str]:
        model = "gpt-4o-mini"
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Project Knowledge:\n{KNOWLEDGE_BLOCK}"},
            *FEW_SHOT,
            {"role": "user", "content": prompt},
        ]
        response = await self.client.responses.create(model=model, input=messages)
        return response.output_text, model
