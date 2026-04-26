import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio import Redis


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, rate_limit: float = 1.0):
        self.redis = redis
        self.rate_limit = rate_limit

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        key = f"throttle:{event.from_user.id}"
        now = time.time()
        last_request = await self.redis.get(key)
        if last_request and now - float(last_request) < self.rate_limit:
            await event.answer("Слишком часто. Подождите 1 секунду.")
            return

        await self.redis.set(key, now, ex=2)
        return await handler(event, data)
