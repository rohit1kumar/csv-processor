import csv
from io import StringIO
from fastapi import UploadFile

required_csv_columns = ["serial_number", "product_name", "input_image_urls"]


def is_valid_csv(csv_file: UploadFile) -> bool:
    """valiadte columns of csv file"""
    try:
        contents = csv_file.file.read().decode("utf-8")
        csv_file.file.seek(0)
        csv_reader = csv.reader(StringIO(contents))
        header = next(csv_reader)
        if header != required_csv_columns:
            return False

        return True
    except (csv.Error, UnicodeDecodeError, Exception) as e:
        print(f"Error reading CSV file: {e}")
        return False
