from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ProductCreate(BaseModel):
    product_id: str = Field(..., max_length=50)
    product_name: str
    batch_no: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class ProductOut(ProductCreate):
    id: int
    qr_path: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True
