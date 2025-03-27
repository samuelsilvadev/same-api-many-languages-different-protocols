from sqlalchemy.orm import Session
import src.models as models
from src.routes.schemas import CreateProductPayload


def create_product(db: Session, body: CreateProductPayload):
    new_product = models.Product(name=body.name, price=body.price, amount=body.amount)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
