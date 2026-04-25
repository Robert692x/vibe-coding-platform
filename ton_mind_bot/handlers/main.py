from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ton_mind_bot.config import settings
from ton_mind_bot.database.models import User
from ton_mind_bot.database.repositories import MessageRepository, PaymentRepository, UserRepository
from ton_mind_bot.keyboards.main import main_menu
from ton_mind_bot.services.dex import DexService
from ton_mind_bot.services.market import MarketService
from ton_mind_bot.services.openai_service import OpenAIService
from ton_mind_bot.services.toncenter import ToncenterService
from ton_mind_bot.utils.texts import t

router = Router()
market_service = MarketService()
toncenter_service = ToncenterService()
openai_service = OpenAIService()
dex_service = DexService()


@router.message(CommandStart())
async def start_handler(message: Message, user: User):
    await message.answer(t(user.language, "start"), reply_markup=main_menu())


@router.message(lambda m: m.text == "English")
async def switch_language(message: Message, user: User, db_session: AsyncSession):
    repo = UserRepository(db_session)
    new_lang = "en" if user.language == "ru" else "ru"
    await repo.set_language(user, new_lang)
    await message.answer(t(new_lang, "lang_switched"))


@router.message(lambda m: m.text in {"Кошелёк", "Wallet"})
async def wallet_screen(message: Message, user: User):
    address = user.wallet or settings.bot_wallet_address
    balance = await toncenter_service.wallet_balance(address)
    txs = await toncenter_service.recent_transactions(address, limit=5)
    tx_rows = "\n".join([f"{tx['date']} | {tx['direction']} | {tx['amount']:.3f} TON" for tx in txs]) or "-"
    await message.answer(t(user.language, "wallet", address=address, balance=balance, txs=tx_rows))


@router.message(lambda m: m.text in {"Цена", "TON Price"})
async def price_screen(message: Message, user: User):
    stats = await market_service.ton_price_stats()
    await message.answer(t(user.language, "price", **stats))


@router.message(lambda m: m.text in {"Киты", "Whales"})
async def whales_screen(message: Message, user: User):
    txs = await toncenter_service.incoming_transactions(settings.bot_wallet_address, limit=100)
    whales = [tx for tx in txs if tx["amount"] >= settings.whale_threshold_ton][:10]
    items = "\n".join([f"{tx['date']} | {tx['amount']:.1f} TON | <code>{tx['hash'][:18]}...</code>" for tx in whales]) or "Нет данных"
    await message.answer(t(user.language, "whales", threshold=int(settings.whale_threshold_ton), items=items))


@router.message(lambda m: m.text == "DEX")
async def dex_screen(message: Message, user: User):
    pools = await dex_service.top_pools()
    rows = "\n".join([f"{p['name']}: TVL ${int(p['tvl'])} | APY {p['apy']}%" for p in pools]) or "Нет данных"
    await message.answer(t(user.language, "dex", pools=rows))


@router.message(lambda m: m.text in {"Аналитика", "Analytics"})
async def analytics_screen(message: Message, user: User):
    address = user.wallet or settings.bot_wallet_address
    balance_ton = await toncenter_service.wallet_balance(address)
    stats = await market_service.ton_price_stats()
    await message.answer(
        t(
            user.language,
            "analytics",
            balance_ton=balance_ton,
            balance_usd=balance_ton * stats["price"],
            ton_price=stats["price"],
        )
    )


@router.message(lambda m: m.text in {"Premium"})
async def premium_screen(message: Message, user: User, db_session: AsyncSession):
    payment = await PaymentRepository(db_session).create_pending(user.id, amount_ton=settings.premium_cost_ton)
    await message.answer(t(user.language, "premium", memo=payment.memo))


@router.message(lambda m: m.text in {"Профиль", "Profile"})
async def profile_screen(message: Message, user: User):
    is_premium = bool(user.premium_until and user.premium_until > datetime.utcnow())
    premium_until = user.premium_until.strftime("%Y-%m-%d") if user.premium_until else "-"
    ref_link = f"https://t.me/{(await message.bot.get_me()).username}?start={user.referral_code}"
    await message.answer(
        t(
            user.language,
            "profile",
            wallet=user.wallet or "-",
            status="Premium" if is_premium else "Free",
            premium_until=premium_until,
            referrals=user.referrals_count,
            ref_link=ref_link,
        )
    )


@router.message(lambda m: m.text in {"Алерты", "Alerts"})
async def alerts_screen(message: Message, user: User, db_session: AsyncSession):
    repo = UserRepository(db_session)
    await repo.toggle_price_alerts(user)
    await repo.toggle_whale_alerts(user)
    await message.answer(
        t(
            user.language,
            "alerts",
            price="ON" if user.price_alerts_enabled else "OFF",
            whales="ON" if user.whale_alerts_enabled else "OFF",
        )
    )


@router.message(lambda m: m.text in {"AI Аналитик", "AI Analyst"})
async def ai_entrypoint(message: Message, user: User):
    await message.answer(t(user.language, "ai_prompt"))


@router.message()
async def ai_chat(message: Message, user: User, db_session: AsyncSession):
    if not message.text:
        return

    is_premium = bool(user.premium_until and user.premium_until > datetime.utcnow())
    if not is_premium and user.ai_requests_today >= 5:
        await message.answer(t(user.language, "limit_reached"))
        return

    answer, model = await openai_service.chat(message.text, premium=is_premium)
    await message.answer(answer)

    user_repo = UserRepository(db_session)
    msg_repo = MessageRepository(db_session)
    if not is_premium:
        await user_repo.increment_ai_requests(user)
    await msg_repo.create(user.id, message.text, answer, model)
