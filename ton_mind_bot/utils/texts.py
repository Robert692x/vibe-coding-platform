TEXTS = {
    "ru": {
        "start": "<b>TON Mind Bot</b>\nAI-аналитик TON блокчейна для трейдеров.",
        "wallet": "<b>Кошелёк</b>\nАдрес: <code>{address}</code>\nБаланс: <b>{balance:.4f} TON</b>\n\nПоследние транзакции:\n{txs}",
        "price": "<b>Цена TON</b>\nКурс: <b>${price:.4f}</b>\n1ч: {change_1h}%\n24ч: {change_24h}%\n7д: {change_7d}%\nОбъём: ${volume}\nКапитализация: ${market_cap}",
        "whales": "<b>Киты</b>\nТранзакции свыше {threshold} TON:\n{items}",
        "dex": "<b>DEX / STON.fi</b>\nТоп пулы:\n{pools}",
        "analytics": "<b>Аналитика</b>\nБаланс: {balance_ton:.4f} TON\nОценка: ${balance_usd:.2f} USD\nЦена TON: ${ton_price:.4f}",
        "premium": (
            "<b>Premium</b>\n"
            "1) Отправьте 5 TON с memo-кодом: <code>{memo}</code>\n"
            "2) Держите 1000 $ALGO\n"
            "3) Пригласите друга (+7 дней)"
        ),
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
        "wallet": "<b>Wallet</b>\nAddress: <code>{address}</code>\nBalance: <b>{balance:.4f} TON</b>\n\nLast transactions:\n{txs}",
        "price": "<b>TON Price</b>\nPrice: <b>${price:.4f}</b>\n1h: {change_1h}%\n24h: {change_24h}%\n7d: {change_7d}%\nVolume: ${volume}\nMarket cap: ${market_cap}",
        "whales": "<b>Whales</b>\nTransactions over {threshold} TON:\n{items}",
        "dex": "<b>DEX / STON.fi</b>\nTop pools:\n{pools}",
        "analytics": "<b>Analytics</b>\nBalance: {balance_ton:.4f} TON\nEstimation: ${balance_usd:.2f}\nTON price: ${ton_price:.4f}",
        "premium": (
            "<b>Premium</b>\n"
            "1) Send 5 TON with memo: <code>{memo}</code>\n"
            "2) Hold 1000 $ALGO\n"
            "3) Invite a friend (+7 days)"
        ),
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
