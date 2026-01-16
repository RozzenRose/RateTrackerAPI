from sqlalchemy import select
from sqlalchemy.sql import func
from app.database.models import BtcUsd, EthUsd


async def get_all_current_rates_form_db(db, currency: str): # достаем из БД все записи
    models = {'btc': BtcUsd, 'eth': EthUsd}
    query = select(models[currency])
    answer = await db.execute(query)
    data = answer.scalars().all()
    return data


async def get_last_current_rates_form_db(db, currency: str): # достаем из БД самую свежую запись
    models = {'btc': BtcUsd, 'eth': EthUsd}
    model = models[currency]

    query = (
        select(model)
        .order_by(model.date_time.desc())
        .limit(1)
    )

    result = await db.execute(query)
    return result.scalars().all()


async def get_interval_rates_form_db(db, currency: str, time_limits): # достаем из БД записи в интервале
    models = {'btc': BtcUsd, 'eth': EthUsd}
    model = models[currency]

    query = select(model).where(model.date_time.between(time_limits.start_date, time_limits.end_date))

    result = await db.execute(query)
    return result.scalars().all()
