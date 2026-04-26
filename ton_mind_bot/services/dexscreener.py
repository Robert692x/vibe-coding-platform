import aiohttp


class DexScreenerService:
    async def ton_pairs(self) -> list[dict]:
        url = "https://api.dexscreener.com/latest/dex/pairs/ton"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as response:
                if response.status != 200:
                    return []
                data = await response.json()
        return data.get("pairs", [])

    async def explosive_tokens(self, min_growth_pct: float, min_market_cap: float, limit: int = 10) -> list[dict]:
        pairs = await self.ton_pairs()
        filtered = []
        for pair in pairs:
            growth = float((pair.get("priceChange") or {}).get("h24") or 0)
            market_cap = float(pair.get("marketCap") or 0)
            if growth >= min_growth_pct and market_cap >= min_market_cap:
                base = pair.get("baseToken") or {}
                filtered.append(
                    {
                        "symbol": base.get("symbol", "?"),
                        "name": base.get("name", "Unknown"),
                        "address": base.get("address", ""),
                        "pair_address": pair.get("pairAddress", ""),
                        "growth_24h": growth,
                        "market_cap": market_cap,
                        "volume_24h": float((pair.get("volume") or {}).get("h24") or 0),
                        "dex": (pair.get("dexId") or "").upper(),
                        "url": pair.get("url", ""),
                    }
                )
        filtered.sort(key=lambda item: item["growth_24h"], reverse=True)
        return filtered[:limit]
