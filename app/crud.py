import uuid
from sqlalchemy.orm import Session
from . import models


def create_request(db: Session, id: uuid.UUID | None) -> models.Request:
    db_request = models.Request(id=id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
