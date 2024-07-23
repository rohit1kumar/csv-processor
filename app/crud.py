import uuid
from sqlalchemy.orm import Session
from . import models


def create_request(db: Session, id: uuid.UUID | None) -> models.Request:
    db_request = models.Request(id=id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_request(db: Session, id: uuid.UUID) -> models.Request:
    return db.query(models.Request).filter(models.Request.id == id).first()
