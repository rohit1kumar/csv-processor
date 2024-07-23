import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, DateTime, UUID, func, Enum

from .database import Base


class StatusEnums(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ERROR = "error"
    PROCESSING = "processing"


class Request(Base):
    __tablename__ = "requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(Enum(StatusEnums), default=StatusEnums.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    products = relationship("Product", back_populates="request")


class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    request_id = Column(UUID(as_uuid=True), ForeignKey("requests.id"))

    request = relationship("Request", back_populates="products")
    images = relationship("Image", back_populates="product")


class Image(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_url = Column(String)
    output_url = Column(String)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))

    product = relationship("Product", back_populates="images")
