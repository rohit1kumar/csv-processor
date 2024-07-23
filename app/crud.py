from sqlalchemy.orm import Session
from . import models


def create_request(db: Session) -> models.Request:
    db_request = models.Request()
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
