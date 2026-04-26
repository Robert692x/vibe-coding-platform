from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ton_mind_bot.config import settings
from ton_mind_bot.database.models import User
from ton_mind_bot.database.repositories import MessageRepository, UserRepository
from ton_mind_bot.keyboards.main import main_menu
from ton_mind_bot.services.dex import DexService
from ton_mind_bot.services.dexscreener import DexScreenerService
from ton_mind_bot.services.holders import HoldersService
from ton_mind_bot.services.market import MarketService
from ton_mind_bot.services.openai_service import OpenAIService
from ton_mind_bot.services.toncenter import ToncenterService
from ton_mind_bot.utils.texts import t

router = Router()
market_service = MarketService()
toncenter_service = ToncenterService()
openai_service = OpenAIService()
dex_service = DexService()
dexscreener_service = DexScreenerService()
holders_service = HoldersService()


def _is_valid_wallet(address: str) -> bool:
    return (address.startswith("EQ") or address.startswith("UQ")) and len(address) >= 40


@router.message(CommandStart())
async def start_handler(message: Message, user: User):
    await message.answer(t(user.language, "start"), reply_markup=main_menu())


@router.message(Command("connect_wallet"))
async def connect_wallet_handler(message: Message, user: User, db_session: AsyncSession):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not _is_valid_wallet(parts[1].strip()):
        await message.answer(t(user.language, "wallet_invalid"))
        return
    wallet = parts[1].strip()
    await UserRepository(db_session).set_wallet(user, wallet)
    await message.answer(t(user.language, "wallet_connected", wallet=wallet))


@router.message(Command("leaderboard"))
@router.message(lambda m: (m.text or "").lower() in {"leaderboard", "топ холдеры", "top holders"})
async def leaderboard_handler(message: Message, user: User):
    holders = await holders_service.top_holders(settings.tracked_jetton_address, limit=10)
    rows = "\n".join([f"#{h['rank']} <code>{h['wallet']}</code> — <b>{h['amount']:.4f}</b>" for h in holders]) or "No data"
    await message.answer(t(user.language, "leaderboard", holders=rows))


@router.message(lambda m: m.text == "English")
async def switch_language(message: Message, user: User, db_session: AsyncSession):
    repo = UserRepository(db_session)
    new_lang = "en" if user.language == "ru" else "ru"
    await repo.set_language(user, new_lang)
    await message.answer(t(new_lang, "lang_switched"))


@router.message(lambda m: m.text in {"Кошелёк", "Wallet"})
async def wallet_screen(message: Message, user: User):
    if not user.wallet:
        await message.answer(t(user.language, "wallet_not_set"))
        return

    balance = await toncenter_service.wallet_balance(user.wallet)
    txs = await toncenter_service.recent_transactions(user.wallet, limit=5)
    tx_rows = "\n".join([f"{tx['date']} | {tx['direction']} | {tx['amount']:.3f} TON" for tx in txs]) or "-"

    algo = await holders_service.wallet_holding(user.wallet, settings.tracked_jetton_address)
    await message.answer(
        t(
            user.language,
            "wallet",
            address=user.wallet,
            balance=balance,
            txs=tx_rows,
            is_holder="YES" if algo["is_holder"] else "NO",
            algo_amount=algo["amount"],
        )
    )


@router.message(lambda m: m.text in {"Цена", "TON Price"})
async def price_screen(message: Message, user: User):
    stats = await market_service.ton_price_stats()
    conversion = await market_service.ton_to_algo_rate()
    await message.answer(
        t(user.language, "price", **stats, ton_in_algo=conversion["ton_in_algo"], algo_usd=conversion["algo_usd"])
    )


@router.message(lambda m: m.text in {"Киты", "Whales"})
async def whales_screen(message: Message, user: User):
    txs = await toncenter_service.incoming_transactions(settings.bot_wallet_address, limit=100)
    whales = [tx for tx in txs if tx["amount"] >= settings.whale_threshold_ton][:10]
    whale_rows = "\n".join(
        [f"{tx['date']} | {tx['amount']:.1f} TON | <code>{tx['source'] or tx['hash'][:18]}...</code>" for tx in whales]
    ) or "Нет данных"

    holders = await holders_service.top_holders(settings.tracked_jetton_address, limit=10)
    holder_rows = "\n".join(
        [f"#{h['rank']} <code>{h['wallet']}</code> — {h['amount']:.4f}" for h in holders]
    ) or "Нет данных"

    await message.answer(
        t(
            user.language,
            "whales",
            threshold=int(settings.whale_threshold_ton),
            items=whale_rows,
            tracked_address=settings.tracked_jetton_address,
            holders=holder_rows,
        )
    )


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
    conversion = await market_service.ton_to_algo_rate()
    await message.answer(
        t(
            user.language,
            "analytics",
            balance_ton=balance_ton,
            balance_usd=balance_ton * stats["price"],
            ton_price=stats["price"],
            balance_algo=balance_ton * conversion["ton_in_algo"],
            ton_in_algo=conversion["ton_in_algo"],
        )
    )


@router.message(lambda m: m.text in {"Premium"})
async def premium_screen(message: Message, user: User):
    await message.answer(t(user.language, "premium_free"))


@router.message(lambda m: m.text in {"Профиль", "Profile"})
async def profile_screen(message: Message, user: User):
    is_premium = False
    premium_until = "Бесплатно / Unlimited"
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


@router.message(lambda m: (m.text or "").lower() in {"токен скан", "token scan"})
async def token_scan_screen(message: Message, user: User, db_session: AsyncSession):
    repo = UserRepository(db_session)
    if not user.price_alerts_enabled:
        await repo.toggle_price_alerts(user)

    tokens = await dexscreener_service.explosive_tokens(
        min_growth_pct=settings.token_growth_threshold_pct,
        min_market_cap=settings.token_market_cap_threshold,
        limit=10,
    )
    if not tokens:
        await message.answer(
            "<b>Токен скан</b>\nСейчас нет монет на TON DEX с ростом 1000%+ и заданной капитализацией.\n"
            "Уведомления включены, отправим сигнал при появлении."
        )
        return

    rows = "\n".join(
        [
            f"• <b>{tkn['symbol']}</b> | {tkn['growth_24h']:.1f}% | MC ${tkn['market_cap']:,.0f}\n{tkn['url']}"
            for tkn in tokens
        ]
    )
    await message.answer("<b>Токен скан (TON)</b>\n" + rows + "\n\nУведомления включены.")


@router.message(lambda m: m.text in {"AI Аналитик", "AI Analyst"})
async def ai_entrypoint(message: Message, user: User):
    await message.answer(t(user.language, "ai_prompt"))


@router.message()
async def ai_chat(message: Message, user: User, db_session: AsyncSession):
    if not message.text:
        return

    answer, model = await openai_service.chat(message.text, premium=True)
    await message.answer(answer)

    user_repo = UserRepository(db_session)
    msg_repo = MessageRepository(db_session)
    await msg_repo.create(user.id, message.text, answer, model)
