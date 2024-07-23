from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, status, UploadFile, Depends

from . import models, crud
from .database import SessionLocal, engine
from .utils.utils import is_valid_csv, required_csv_columns

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_csv(file: UploadFile | None = None, db: Session = Depends(get_db)):
    """Upload a CSV file, validate it, create a request in db then process it using celery worker"""
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No upload file sent",
        )

    if file.content_type != "text/csv":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File must be CSV",
        )
    if not is_valid_csv(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV file, must have columns: {required_csv_columns}",
        )
    try:
        # upload to s3
        request = crud.create_request(db)
        return {"detail": "File uploaded, getting processed", "request_id": request.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
