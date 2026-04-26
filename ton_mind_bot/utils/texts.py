TEXTS = {
    "ru": {
        "start": "<b>TON Mind Bot</b>\nAI-аналитик TON блокчейна для трейдеров.",
        "wallet": (
            "<b>Кошелёк</b>\nАдрес: <code>{address}</code>\nБаланс: <b>{balance:.4f} TON</b>\n"
            "ALGO holder: <b>{is_holder}</b>\nALGO amount: <b>{algo_amount:.4f}</b>\n\nПоследние транзакции:\n{txs}"
        ),
        "wallet_not_set": "Кошелёк не подключен. Используйте: <code>/connect_wallet EQ...</code>",
        "wallet_connected": "✅ Кошелёк подключен: <code>{wallet}</code>",
        "wallet_invalid": "❌ Неверный формат кошелька. Пример: <code>/connect_wallet EQ...</code>",
        "price": (
            "<b>Цена TON</b>\nКурс: <b>${price:.4f}</b>\n1ч: {change_1h}%\n24ч: {change_24h}%\n7д: {change_7d}%\n"
            "Объём: ${volume}\nКапитализация: ${market_cap}\n\n1 TON = <b>{ton_in_algo:.4f} ALGO</b>\nALGO: ${algo_usd:.4f}"
        ),
        "whales": (
            "<b>Киты</b>\nТранзакции свыше {threshold} TON:\n{items}\n\n"
            "<b>Топ-10 холдеров</b>\nJetton: <code>{tracked_address}</code>\n{holders}"
        ),
        "leaderboard": "<b>Leaderboard TOP-10 ALGO holders</b>\n{holders}",
        "dex": "<b>DEX / STON.fi</b>\nТоп пулы:\n{pools}",
        "analytics": (
            "<b>Аналитика</b>\nБаланс: {balance_ton:.4f} TON\nОценка: ${balance_usd:.2f} USD\n"
            "Цена TON: ${ton_price:.4f}\nБаланс: {balance_algo:.4f} ALGO\n1 TON = {ton_in_algo:.4f} ALGO"
        ),
        "premium_free": "<b>Free Access</b>\nВсе функции бота теперь полностью бесплатны без подписки и оплат.",
        "profile": (
            "<b>Профиль</b>\nКошелёк: <code>{wallet}</code>\n"
            "Статус: <b>{status}</b>\nPremium до: {premium_until}\n"
            "Рефералы: {referrals}\nСсылка: {ref_link}"
        ),
        "alerts": "<b>Алерты</b>\nЦеновые: {price}\nКиты: {whales}",
        "ai_prompt": "<b>AI Аналитик</b>\nОтправьте ваш вопрос по TON.",
        "lang_switched": "Язык переключен на English.",
        "limit_reached": "Дневной лимит исчерпан. Оформите Premium.",
        "throttled": "Слишком часто. Подождите 1 секунду.",
        "banned": "Ваш аккаунт заблокирован.",
    },
    "en": {
        "start": "<b>TON Mind Bot</b>\nAI analyst for TON traders.",
        "wallet": (
            "<b>Wallet</b>\nAddress: <code>{address}</code>\nBalance: <b>{balance:.4f} TON</b>\n"
            "ALGO holder: <b>{is_holder}</b>\nALGO amount: <b>{algo_amount:.4f}</b>\n\nLast transactions:\n{txs}"
        ),
        "wallet_not_set": "Wallet is not connected. Use: <code>/connect_wallet EQ...</code>",
        "wallet_connected": "✅ Wallet connected: <code>{wallet}</code>",
        "wallet_invalid": "❌ Invalid wallet format. Example: <code>/connect_wallet EQ...</code>",
        "price": (
            "<b>TON Price</b>\nPrice: <b>${price:.4f}</b>\n1h: {change_1h}%\n24h: {change_24h}%\n7d: {change_7d}%\n"
            "Volume: ${volume}\nMarket cap: ${market_cap}\n\n1 TON = <b>{ton_in_algo:.4f} ALGO</b>\nALGO: ${algo_usd:.4f}"
        ),
        "whales": (
            "<b>Whales</b>\nTransactions over {threshold} TON:\n{items}\n\n"
            "<b>Top 10 Holders</b>\nJetton: <code>{tracked_address}</code>\n{holders}"
        ),
        "leaderboard": "<b>Leaderboard TOP-10 ALGO holders</b>\n{holders}",
        "dex": "<b>DEX / STON.fi</b>\nTop pools:\n{pools}",
        "analytics": (
            "<b>Analytics</b>\nBalance: {balance_ton:.4f} TON\nEstimation: ${balance_usd:.2f}\n"
            "TON price: ${ton_price:.4f}\nBalance: {balance_algo:.4f} ALGO\n1 TON = {ton_in_algo:.4f} ALGO"
        ),
        "premium_free": "<b>Free Access</b>\nAll bot features are now fully free with no subscription or payment.",
        "profile": (
            "<b>Profile</b>\nWallet: <code>{wallet}</code>\n"
            "Status: <b>{status}</b>\nPremium until: {premium_until}\n"
            "Referrals: {referrals}\nLink: {ref_link}"
        ),
        "alerts": "<b>Alerts</b>\nPrice: {price}\nWhales: {whales}",
        "ai_prompt": "<b>AI Analyst</b>\nSend your TON-related question.",
        "lang_switched": "Language switched to Russian.",
        "limit_reached": "Daily free limit reached. Get Premium.",
        "throttled": "Too many requests. Wait 1 second.",
        "banned": "Your account is banned.",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    language = lang if lang in TEXTS else "ru"
    template = TEXTS[language][key]
    return template.format(**kwargs)
