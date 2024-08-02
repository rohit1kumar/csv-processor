import requests
from datetime import datetime, timezone
from app.models import StatusEnums


def trigger_webhook(url, request_id):
    try:
        webhook_json = {
            "request_id": str(request_id),
            "status": StatusEnums.COMPLETED.value,
            "timestamp": str(datetime.now(timezone.utc)),
        }
        response = requests.post(url, json=webhook_json)
        response.raise_for_status()
        print(f"Webhook triggered for request: {request_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error triggering webhook for request: {request_id}, {e}")
