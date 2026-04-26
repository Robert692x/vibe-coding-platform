import asyncio

from aiogram import Bot
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from ton_mind_bot.config import settings
from ton_mind_bot.database.repositories import UserRepository
from ton_mind_bot.services.dexscreener import DexScreenerService


class TokenGrowthNotifier:
    def __init__(self, bot: Bot, session_factory: async_sessionmaker, redis: Redis):
        self.bot = bot
        self.session_factory = session_factory
        self.redis = redis
        self.service = DexScreenerService()
        self.redis_key = "token_scan:notified"

    async def run(self) -> None:
        while True:
            tokens = await self.service.explosive_tokens(
                min_growth_pct=settings.token_growth_threshold_pct,
                min_market_cap=settings.token_market_cap_threshold,
                limit=20,
            )
            async with self.session_factory() as session:
                users = await UserRepository(session).get_price_alert_users()
                for token in tokens:
                    dedup_key = f"{token['pair_address']}:{int(token['growth_24h'])}"
                    if await self.redis.sismember(self.redis_key, dedup_key):
                        continue
                    await self.redis.sadd(self.redis_key, dedup_key)
                    text = (
                        "🚀 <b>Token Scan Alert (TON)</b>\n"
                        f"<b>{token['name']} ({token['symbol']})</b>\n"
                        f"Рост 24ч: <b>{token['growth_24h']:.2f}%</b>\n"
                        f"Капитализация: <b>${token['market_cap']:,.0f}</b>\n"
                        f"Объём 24ч: <b>${token['volume_24h']:,.0f}</b>\n"
                        f"DEX: <b>{token['dex']}</b>\n"
                        f"Адрес: <code>{token['address']}</code>\n"
                        f"Ссылка: {token['url']}"
                    )
                    for user in users:
                        await self.bot.send_message(user.telegram_id, text)
            await asyncio.sleep(30)
