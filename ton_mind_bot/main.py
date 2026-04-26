import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from redis.asyncio import Redis

from ton_mind_bot.config import settings
from ton_mind_bot.database.session import init_models, session_factory
from ton_mind_bot.handlers.main import router
from ton_mind_bot.middleware.auth import AuthMiddleware
from ton_mind_bot.middleware.throttle import ThrottleMiddleware
from ton_mind_bot.services.wallet_activity_scanner import WalletActivityScanner
from ton_mind_bot.services.token_growth_notifier import TokenGrowthNotifier


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await init_models()

    bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)
    redis = Redis.from_url(settings.redis_url, decode_responses=True)

    dp = Dispatcher()
    dp.update.middleware(AuthMiddleware(session_factory))
    dp.message.middleware(ThrottleMiddleware(redis))
    dp.include_router(router)

    activity_scanner = WalletActivityScanner(bot, session_factory, redis)
    activity_scanner_task = asyncio.create_task(activity_scanner.run())
    token_notifier = TokenGrowthNotifier(bot, session_factory, redis)
    token_notifier_task = asyncio.create_task(token_notifier.run())

    try:
        await dp.start_polling(bot)
    finally:
        activity_scanner_task.cancel()
        token_notifier_task.cancel()
        await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
