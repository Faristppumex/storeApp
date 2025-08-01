from celery import Celery

celery = Celery(
    'storeApp',
    broker='pyamqp://guest:guest@localhost:5672//',  # Update with your RabbitMQ URL
    backend='rpc://'
)

# task_serializer = 'json'
# result_serializer='json'
# accept_content=['json']
# timezone = 'Asia/kochi'
# enable_utc = True
import tasks