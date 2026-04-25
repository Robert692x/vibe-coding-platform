import aiohttp


class MarketService:
    async def ton_price_stats(self) -> dict:
        url = "https://api.coingecko.com/api/v3/coins/the-open-network"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                response.raise_for_status()
                data = await response.json()
        market = data["market_data"]
        return {
            "price": market["current_price"]["usd"],
            "change_1h": market["price_change_percentage_1h_in_currency"]["usd"],
            "change_24h": market["price_change_percentage_24h_in_currency"]["usd"],
            "change_7d": market["price_change_percentage_7d_in_currency"]["usd"],
            "volume": int(market["total_volume"]["usd"]),
            "market_cap": int(market["market_cap"]["usd"]),
        }
