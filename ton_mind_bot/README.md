# TON Mind Bot

Production-ready async Telegram bot (aiogram 3.7) for TON blockchain analytics.

## Stack
- Python 3.12
- aiogram 3.7
- PostgreSQL 16
- Redis 7
- OpenAI API
- Toncenter API

- DexScreener token scan: active TON tokens with growth 1000%+ and market-cap threshold notifications.
## Run locally
```bash
cp .env.example .env
# fill secrets
pip install -r requirements.txt
python -m ton_mind_bot.main
```

## Docker
```bash
docker compose up --build
```
