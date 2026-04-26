from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from ton_mind_bot.database.repositories import UserRepository


class AuthMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = data.get("event_from_user")
        if not telegram_user:
            return await handler(event, data)

        async with self.session_factory() as session:
            repo = UserRepository(session)
            user = await repo.get_or_create(telegram_user.id)
            if user.is_banned:
                if hasattr(event, "answer"):
                    await event.answer("Ваш аккаунт заблокирован.")
                return
            await repo.reset_expired_premium(user)
            data["db_session"] = session
            data["user"] = user
            return await handler(event, data)
