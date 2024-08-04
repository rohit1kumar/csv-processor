# Image Processing Service
Processes CSV files containing product data and images, compresses the images, and stores the results.

## Components
- FastAPI: Web server for handling API requests
- Celery: Task queue for async processing
- PostgreSQL: Database for storing product data
- S3: Object storage for image uploads
- RabbitMQ: Message broker for Celery

![architecture](https://github.com/user-attachments/assets/c5d3c232-cb45-4c3b-9d7a-aab8b704710c)

FastAPI server receives CSV files with webhook URL, validates them, stores in S3, and creates a database entry. It pushes the task to RabbitMQ and returns a request ID.
Celery worker processes the CSV, compresses images, uploads to S3, updates the database, and notifies via webhook.
Clients can check status using the request ID.


## API Endpoints (Visit `/docs`)

`POST /api/v1/upload`: Upload CSV file + webhook URL (optional)

`GET /api/v1/status/{request_id}`: Check processing status



## Database Schema

![database_schema)](https://github.com/user-attachments/assets/5516d92d-d0ae-42aa-bbf0-ce273a53e723)

## Asynchronous Processing
Celery worker handles:

1. CSV parsing
2. Image downloading and compression
3. S3 uploads
4. Database updates
5. Webhook notifications

## How to Run
1. Get the code: `git clone https://github.com/rohit1kumar/csv-processor.git`
2. Install dependencies using poetry: `poetry install`
3. Add environment variables to `.env` file (see `.env.example`)
4. Run the FastAPI server: `./scripts/start_server.sh` *(dont forget to make the script executable)*
5. Run the Celery worker: `./scripts/start_celery.sh`



