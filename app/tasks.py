import os
import uuid
from celery import Celery
from dotenv import load_dotenv

from .utils.aws import S3
from .utils.image_processing import compress_image, get_csv_data
from .database import SessionLocal
from .models import Request, Product, Image, StatusEnums

load_dotenv()

BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672/vhost")

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

            for row in get_csv_data(file):
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
                for url in input_image_urls.split(","):
                    try:
                        image_buffer = compress_image(url)
                        image_id = uuid.uuid4()
                        image_name = f"images/compressed/{image_id}.jpg"
                        s3.upload_file(image_buffer, image_name)

                        image_data = {
                            "id": image_id,
                            "input_url": url,
                            "product_id": product_id,
                            "output_url": s3.get_file_url(image_name),
                        }
                        db_image = Image(**image_data)
                        db.add(db_image)
                        db.commit()
                        db.refresh(db_image)
                    except Exception as e:
                        print("Error processing image", e)
                        continue

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
