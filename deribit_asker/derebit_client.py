import aiohttp
from typing import Dict, Optional
import asyncio
from config import settings


class DeribitClient:
    """Асинхронный клиент для API Deribit"""

    BASE_URL = settings.deribit_api_url

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_index_price(self, index_name: str) -> float:
        """Получить индексную цену"""
        url = f"{self.BASE_URL}/public/get_index_price"
        params = {"index_name": index_name}

        async with self.session.get(url, params=params, timeout=10) as response:
            response.raise_for_status()
            data = await response.json()
            return data['result']['index_price']

    async def get_prices(self, tickers: list) -> Dict[str, float]:
        """Получить цены для нескольких тикеров параллельно"""
        tasks = []
        for ticker in tickers:
            tasks.append(self.get_index_price(ticker))

        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))