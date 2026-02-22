from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    batch_no = Column(String(100))
    description = Column(Text)
    price = Column(DECIMAL(12,2))
    company_name = Column(String(255))
    phone = Column(String(50))
    website = Column(String(255))
    email = Column(String(255))
    address = Column(Text)
    qr_path = Column(String(1024))
    created_at = Column(TIMESTAMP)
