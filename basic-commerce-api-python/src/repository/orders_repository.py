from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from src import models
from src.config import log_sql

from src.config import logging_instance
from src.routes.schemas import CreateOrderPayload, OrderProduct

from src.repository import order_products_repository


def get_all_orders_by_user(db: Session, user_id):
    query = db.query(models.Order).filter(models.Order.user_id == user_id)

    log_sql(query)

    return query.all()


def get_order_by_id(db: Session, id: int):
    query = db.query(models.Order).filter(models.Order.id == id)

    log_sql(query)

    return query.first()


def get_order_by_id_and_user(db: Session, id: int, user_id: int):
    query = db.query(models.Order).filter(
        models.Order.id == id and models.Order.user_id == user_id
    )

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


def update_order_with_products(
    db: Session, order: models.Order, products: List[OrderProduct]
):
    try:
        logging_instance.info("Updating the order.")

        order.updated_at = datetime.utcnow()
        order_products = []

        db.flush()

        logging_instance.info(f"Order with id {order.id} updated.")

        if products is not None and len(products) > 0:
            logging_instance.info("Starting to remove previous products.")

            order_products_repository.remove_products_by_order(db, order.id)

            logging_instance.info("Starting to insert products.")

            order_products = [
                models.OrderProduct(
                    order_id=order.id,
                    product_id=product.product_id,
                    price=product.price,
                )
                for product in products
            ]

            db.add_all(order_products)

        logging_instance.info("Commiting changes.")

        db.commit()

        return (order, order_products)
    except Exception as error:
        db.rollback()
        raise error
