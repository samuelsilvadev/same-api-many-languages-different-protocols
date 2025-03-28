from sqlalchemy.orm import Session

from src import models
from src.config import log_sql

from src.config import logging_instance
from src.routes.schemas import CreateOrderPayload


def get_all_orders_by_user(db: Session, user_id):
    query = db.query(models.Order).filter(models.Order.user_id == user_id)

    log_sql(query)

    return query.all()


def get_order_by_id(db: Session, id: int):
    query = db.query(models.Order).filter(models.Order.id == id)

    log_sql(query)

    return query.first()


def create_order_with_products(db: Session, order: CreateOrderPayload):
    try:
        logging_instance.info("Creating the order.")

        new_order = models.Order(user_id=order.user_id)
        order_products = []

        db.add(new_order)
        db.flush()

        logging_instance.info(f"Order with id {new_order.id} created.")

        if order.products is not None:
            logging_instance.info("Starting to insert products.")

            order_products = [
                models.OrderProduct(
                    order_id=new_order.id,
                    product_id=product.product_id,
                    price=product.price,
                )
                for product in order.products
            ]

            db.add_all(order_products)

        logging_instance.info("Commiting.")

        db.commit()

        return (new_order, order_products)
    except Exception as error:
        db.rollback()
        raise error
