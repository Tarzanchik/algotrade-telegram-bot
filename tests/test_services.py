import pytest
from aioresponses import aioresponses
import datetime as dt
from bot.services import get_intraday, MarketDataError

@pytest.mark.asyncio
async def test_get_intraday_ok(monkeypatch):
    monkeypatch.setenv("FINAGE_API_KEY", "TESTKEY")
    url = "https://api.finage.co.uk/agg/stock/AAPL/intraday/5min?apikey=TESTKEY"
    payload = {"results": [{"t": 1724500000000, "c": 100.5}]}
    with aioresponses() as m:
        m.get(url, payload=payload)
        rows = await get_intraday("AAPL", "5min")
    assert len(rows) == 1
    ts, close = rows[0]
    assert isinstance(ts, dt.datetime)
    assert close == 100.5

@pytest.mark.asyncio
async def test_get_intraday_no_key(monkeypatch):
    monkeypatch.delenv("FINAGE_API_KEY", raising=False)
    with pytest.raises(MarketDataError):
        await get_intraday("AAPL")
