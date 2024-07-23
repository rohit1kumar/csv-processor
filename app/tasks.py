import os
import uuid
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672/")

celery_app = Celery(__name__, broker=BROKER_URL)

# Configure Celery
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(name="process_csv")
def process_csv(file_name: str, request_id: uuid.UUID):
    print(file_name, request_id)


if __name__ == "__main__":
    celery_app.start()
