import os
import csv
import uuid
from io import StringIO
from celery import Celery
from dotenv import load_dotenv

from .database import SessionLocal
from .models import Request, Product, StatusEnums
from .utils.aws import S3

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
    """Process the CSV file and create products in db & store compressed images in S3"""

    s3 = S3()
    with SessionLocal() as db:
        try:
            db_request = db.query(Request).filter(Request.id == request_id).first()
            if db_request is None:
                print(f"Request with id {request_id} not found!")
                return

            print(f"Worker picked request: {request_id}")
            db_request.status = StatusEnums.PROCESSING
            db.commit()

            file = s3.download_file(file_name)
            data = file["Body"].read().decode("utf-8")
            reader = csv.reader(StringIO(data))
            next(reader)  # Skip header

            for row in reader:
                serial_number, product_name, input_image_urls = row
                product_data = {
                    "serial_number": serial_number,
                    "name": product_name,
                    "request_id": request_id,
                }
                db_product = Product(**product_data)
                db.add(db_product)
                db.commit()
                db.refresh(db_product)

                product_id = db_product.id
                print(f"Created product : {product_id}")

            db_request.status = StatusEnums.COMPLETED
            db.commit()
            print(f"Processing completed for request: {request_id}")

        except Exception as e:
            db_request.status = StatusEnums.ERROR
            db.commit()
            print("Error in worker: ", e)
            return


if __name__ == "__main__":
    celery_app.start()
