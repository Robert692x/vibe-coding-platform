from datetime import datetime

import aiohttp

from ton_mind_bot.config import settings


class ToncenterService:
    def __init__(self) -> None:
        self.base_url = settings.toncenter_base_url
        self.api_key = settings.toncenter_api_key

    async def _get(self, method: str, params: dict) -> dict:
        query = {**params, "api_key": self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/{method}", params=query, timeout=15) as response:
                response.raise_for_status()
                return await response.json()

    async def wallet_balance(self, address: str) -> float:
        data = await self._get("getAddressBalance", {"address": address})
        nanotons = int(data["result"])
        return nanotons / 1e9

    async def recent_transactions(self, address: str, limit: int = 5) -> list[dict]:
        data = await self._get("getTransactions", {"address": address, "limit": limit})
        txs = []
        for tx in data.get("result", []):
            amount = abs(int(tx.get("in_msg", {}).get("value", 0)) / 1e9)
            inbound = tx.get("in_msg", {}).get("destination") == address
            txs.append(
                {
                    "date": datetime.utcfromtimestamp(tx["utime"]).strftime("%Y-%m-%d %H:%M"),
                    "direction": "IN" if inbound else "OUT",
                    "amount": amount,
                    "hash": tx["transaction_id"]["hash"],
                    "comment": tx.get("in_msg", {}).get("message", ""),
                }
            )
        return txs

    async def incoming_transactions(self, address: str, limit: int = 50) -> list[dict]:
        txs = await self.recent_transactions(address, limit=limit)
        return [tx for tx in txs if tx["direction"] == "IN"]
