import secrets
import string
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ton_mind_bot.config import settings
from ton_mind_bot.database.models import Message, Payment, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, telegram_id: int) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user

        referral_code = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        user = User(telegram_id=telegram_id, referral_code=referral_code)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def reset_expired_premium(self, user: User) -> None:
        if user.premium_until and user.premium_until.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            user.premium_until = None
            await self.session.commit()

    async def increment_ai_requests(self, user: User) -> None:
        user.ai_requests_today += 1
        await self.session.commit()

    async def set_language(self, user: User, language: str) -> None:
        user.language = language
        await self.session.commit()

    async def set_wallet(self, user: User, wallet: str) -> None:
        user.wallet = wallet
        await self.session.commit()

    async def toggle_whale_alerts(self, user: User) -> None:
        user.whale_alerts_enabled = not user.whale_alerts_enabled
        await self.session.commit()

    async def toggle_price_alerts(self, user: User) -> None:
        user.price_alerts_enabled = not user.price_alerts_enabled
        await self.session.commit()


    async def get_alert_users(self) -> list[User]:
        result = await self.session.execute(select(User).where(User.whale_alerts_enabled.is_(True)))
        return list(result.scalars().all())

    async def get_price_alert_users(self) -> list[User]:
        result = await self.session.execute(select(User).where(User.price_alerts_enabled.is_(True)))
        return list(result.scalars().all())
    async def activate_premium(self, user: User, days: int | None = None) -> None:
        period = days or settings.premium_days
        base = user.premium_until if user.premium_until and user.premium_until > datetime.utcnow() else datetime.utcnow()
        user.premium_until = base + timedelta(days=period)
        await self.session.commit()


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, prompt: str, response: str, model: str) -> Message:
        message = Message(user_id=user_id, prompt=prompt, response=response, model=model)
        self.session.add(message)
        await self.session.commit()
        return message


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_pending(self, user_id: int, amount_ton: float = 5) -> Payment:
        memo = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        payment = Payment(user_id=user_id, memo=memo, amount_ton=amount_ton, status="pending")
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_pending(self) -> list[Payment]:
        result = await self.session.execute(select(Payment).where(Payment.status == "pending"))
        return list(result.scalars().all())

    async def mark_paid(self, payment: Payment, tx_hash: str) -> None:
        payment.status = "paid"
        payment.tx_hash = tx_hash
        await self.session.commit()
