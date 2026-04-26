import asyncio

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from ton_mind_bot.config import settings
from ton_mind_bot.database.repositories import PaymentRepository, UserRepository
from ton_mind_bot.services.toncenter import ToncenterService


async def run_payment_scanner(bot: Bot, session_factory: async_sessionmaker) -> None:
    toncenter = ToncenterService()
    while True:
        async with session_factory() as session:
            payment_repo = PaymentRepository(session)
            user_repo = UserRepository(session)
            pending = await payment_repo.get_pending()
            if pending:
                incoming = await toncenter.incoming_transactions(settings.bot_wallet_address, limit=100)
                for payment in pending:
                    for tx in incoming:
                        if tx.get("comment", "").strip() == payment.memo and tx["amount"] >= payment.amount_ton:
                            await payment_repo.mark_paid(payment, tx["hash"])
                            user = await user_repo.get_by_id(payment.user_id)
                            if user:
                                await user_repo.activate_premium(user)
                                await bot.send_message(user.telegram_id, "✅ Premium активирован автоматически.")
                            break
        await asyncio.sleep(30)
