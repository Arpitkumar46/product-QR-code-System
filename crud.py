from sqlalchemy.orm import Session
from . import models

def create_product(db: Session, product_data: dict):
    p = models.Product(
        product_id=product_data.get('product_id'),
        product_name=product_data.get('product_name'),
        batch_no=product_data.get('batch_no'),
        description=product_data.get('description'),
        price=product_data.get('price'),
        company_name=product_data.get('company_name'),
        phone=product_data.get('phone'),
        website=product_data.get('website'),
        email=product_data.get('email'),
        address=product_data.get('address'),
        qr_path=product_data.get('qr_path'),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_by_product_id(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()

def list_products(db: Session, limit: int = 100, search: str = None):
    q = db.query(models.Product).order_by(models.Product.created_at.desc())
    if search:
        like = f"%{search}%"
        q = q.filter((models.Product.product_id.ilike(like)) | (models.Product.product_name.ilike(like)))
    return q.limit(limit).all()

def delete_product(db: Session, product_id: str):
    p = get_by_product_id(db, product_id)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True

def last_50(db: Session):
    return db.query(models.Product).order_by(models.Product.created_at.desc()).limit(50).all()
