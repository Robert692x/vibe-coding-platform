import aiohttp


class DexService:
    async def top_pools(self) -> list[dict]:
        # Placeholder endpoint; adapt to official STON.fi API in production.
        url = "https://api.ston.fi/v1/pools"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                if response.status != 200:
                    return []
                data = await response.json()
        pools = data.get("data", [])[:5]
        return [{"name": p.get("name", "N/A"), "tvl": p.get("tvlUsd", 0), "apy": p.get("apy", 0)} for p in pools]
