from sqlalchemy.orm import Session

from src import models
from src.config import log_sql


def remove_products_by_order(db: Session, order_id: int):
    query = db.query(models.OrderProduct).filter(
        models.OrderProduct.order_id == order_id
    )

    log_sql(query)

    return query.delete()
