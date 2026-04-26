import aiohttp

from ton_mind_bot.config import settings


class HoldersService:
    async def top_holders(self, jetton_address: str | None = None, limit: int = 10) -> list[dict]:
        target = jetton_address or settings.tracked_jetton_address
        url = f"{settings.tonapi_base_url}/jettons/{target}/holders"
        params = {"limit": limit, "offset": 0}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=20) as response:
                if response.status != 200:
                    return []
                data = await response.json()

        holders = []
        for idx, item in enumerate(data.get("addresses", [])[:limit], start=1):
            owner = item.get("owner", {})
            holders.append(
                {
                    "rank": idx,
                    "wallet": owner.get("address", "unknown"),
                    "amount": float(item.get("balance", 0)),
                }
            )
        return holders

    async def wallet_holding(self, wallet_address: str, jetton_address: str | None = None) -> dict:
        holders = await self.top_holders(jetton_address=jetton_address, limit=1000)
        for holder in holders:
            if holder["wallet"] == wallet_address:
                return {"is_holder": True, "amount": holder["amount"], "rank": holder["rank"]}
        return {"is_holder": False, "amount": 0.0, "rank": None}
