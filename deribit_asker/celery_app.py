# worker/celery_app.py
from celery import Celery
from config import settings
from celery.schedules import crontab
from kombu import Queue, Exchange


# Создаем Celery app с RabbitMQ как брокер
celery_app = Celery(
    'deribit_asker',
    broker=settings.rabbitmq_url,  # RabbitMQ URL
    #backend=settings.redis_url,  # Redis для результатов
    include=['deribit_asker.tasks']  # Где искать задачи
)

# Конфигурация
celery_app.conf.update(
    beat_schedule={ #запускаем воркер сбора данных каждую минуту
        'fetch-deribit-prices-every-minute': {
            'task': 'tasks.fetch_prices_task',
            'schedule': crontab(minute='*')}
    },
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,

    # Настройки воркера
    worker_prefetch_multiplier=1,  # По одной задаче за раз
    task_acks_late=True,  # Подтверждать после выполнения
    task_reject_on_worker_lost=True,

    # Очереди
    task_default_queue='dispatch',
    task_queues=[
        Queue('prices', Exchange('prices'), routing_key='prices')
    ],
    task_routes={
        'tasks.fetch_prices_task': {'queue': 'prices'},
    }
)
