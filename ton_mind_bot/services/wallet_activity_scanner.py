import asyncio

from aiogram import Bot
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from ton_mind_bot.config import settings
from ton_mind_bot.database.repositories import UserRepository
from ton_mind_bot.services.toncenter import ToncenterService


class WalletActivityScanner:
    def __init__(self, bot: Bot, session_factory: async_sessionmaker, redis: Redis):
        self.bot = bot
        self.session_factory = session_factory
        self.redis = redis
        self.toncenter = ToncenterService()
        self.seen_key = "scanner:seen_wallet_txs"

    def _detect_action(self, tx: dict) -> str:
        comment = (tx.get("comment") or "").lower()
        if "swap" in comment or "ston.fi" in comment:
            return "SWAP"
        if tx.get("direction") == "IN":
            return "BUY"
        return "SELL"

    async def run(self) -> None:
        while True:
            txs = await self.toncenter.recent_transactions(settings.tracked_wallet_address, limit=20)
            async with self.session_factory() as session:
                users = await UserRepository(session).get_alert_users()
                for tx in txs:
                    if await self.redis.sismember(self.seen_key, tx["hash"]):
                        continue

                    await self.redis.sadd(self.seen_key, tx["hash"])
                    action = self._detect_action(tx)
                    text = (
                        f"📡 <b>Скан активности</b>\n"
                        f"Кошелёк: <code>{settings.tracked_wallet_address}</code>\n"
                        f"Действие: <b>{action}</b>\n"
                        f"Сумма: <b>{tx['amount']:.3f} TON</b>\n"
                        f"Дата: {tx['date']}\n"
                        f"TX: <code>{tx['hash'][:24]}...</code>"
                    )
                    for user in users:
                        await self.bot.send_message(user.telegram_id, text)
            await asyncio.sleep(30)
