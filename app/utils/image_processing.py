import csv
import requests
from io import StringIO, BytesIO
from PIL import Image as PILImage


def compress_image(url: str) -> BytesIO:
    response = requests.get(url)
    with PILImage.open(BytesIO(response.content)) as pil_image:
        buffer = BytesIO()
        format = pil_image.format
        pil_image.save(buffer, format=format, quality=44, optimize=True)
        buffer.seek(0)
        return buffer


def get_csv_data(file) -> list:
    data = file["Body"].read().decode("utf-8")
    reader = csv.reader(StringIO(data))
    next(reader)  # Skip header
    return list(reader)
