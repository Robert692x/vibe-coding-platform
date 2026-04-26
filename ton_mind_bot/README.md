# TON Mind Bot

Production-ready async Telegram bot (aiogram 3.7) for TON blockchain analytics.

## Stack
- Python 3.12
- aiogram 3.7
- PostgreSQL 16
- Redis 7
- OpenAI API
- Toncenter API
- TonAPI API (top holders)

## Key features
- All bot functions are fully free (no premium paywall).
- TON price, market stats and TON→ALGO conversion.
- Top whale transactions and top-10 holders for tracked Jetton.
- Wallet activity scanner for tracked wallet (BUY/SELL/SWAP notifications).
- DexScreener token scan: active TON tokens with growth 1000%+ and market-cap threshold notifications.
- No payment required: premium flow disabled in active UX.

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

## Extra commands
- `/connect_wallet EQ...` — connect user wallet for ALGO holder analysis.
- `/leaderboard` — show top-10 ALGO holders leaderboard.


## LLM setup
- Master system prompt + knowledge + few-shot are in `ton_mind_bot/ai/system_prompt.py`.
- Extended architecture notes: `ton_mind_bot/LLM_ARCHITECTURE.md`.
- Knowledge base document: `ton_mind_bot/ai/knowledge_base.md`.
