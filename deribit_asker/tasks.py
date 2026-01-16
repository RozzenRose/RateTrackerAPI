from celery import Celery, shared_task
import asyncio
from deribit_asker.derebit_client import DeribitClient
from app.database.engine import session_factory
from app.database.models import BtcUsd, EthUsd
from sqlalchemy import insert


@shared_task(name="tasks.fetch_prices_task") # задача для получения цен
def fetch_prices_task():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_fetch_prices()) #асинхронно вызываем функцию сбора данных


async def save_prices(db, prices):
    querry = insert(BtcUsd).values(rate=prices['btc_usd']) # вставляем данные в бд по btc
    await db.execute(querry)
    querry = insert(EthUsd).values(rate=prices['eth_usd']) # вставляем данные в бд по eth
    await db.execute(querry)
    await db.commit()


async def _fetch_prices():
    async with DeribitClient() as client:
        prices = await client.get_prices(['btc_usd', 'eth_usd']) # получаем цены через клиент
        async with session_factory() as session:
            await save_prices(session, prices) # сохраняем цены в БД



# workers
# celery -A deribit_asker.celery_app worker -Q prices -c 8

# beat
# celery -A deribit_asker.celery_app beat
