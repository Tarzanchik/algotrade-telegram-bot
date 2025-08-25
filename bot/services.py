# bot/services.py
import os
import aiohttp
import datetime as dt
from typing import List, Tuple

class MarketDataError(Exception):
    ...

async def get_intraday(ticker: str, interval: str = "5min") -> List[Tuple[dt.datetime, float]]:
    finage_api = os.getenv("FINAGE_API_KEY")  # читаем ключ при каждом вызове (on call)
    if not finage_api:
        raise MarketDataError("FINAGE_API_KEY is not set")

    url = f"https://api.finage.co.uk/agg/stock/{ticker}/intraday/{interval}?apikey={finage_api}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()
    return [(dt.datetime.fromtimestamp(c["t"] / 1000), c["c"]) for c in data["results"]]
