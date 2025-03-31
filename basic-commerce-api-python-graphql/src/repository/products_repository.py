from sqlalchemy.orm import Session
import src.models as models
from src.routes.schemas import CreateProductPayload
from src.config import log_sql


def create_product(db: Session, body: CreateProductPayload):
    new_product = models.Product(name=body.name, price=body.price, amount=body.amount)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_product_by_id(db: Session, id: int):
    query = db.query(models.Product).filter(models.Product.id == id)

    log_sql(query)

    return query.first()


def get_all_products(db: Session):
    return db.query(models.Product).all()
