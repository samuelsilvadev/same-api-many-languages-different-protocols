from sqlalchemy.orm import Session
from src.routes.schemas import CreateUserPayload
import src.models as models
import src.security as security


def create_user(db: Session, body: CreateUserPayload):
    password_hash = security.build_password_hash(body.password)
    new_user = models.User(
        name=body.name, email=body.email, password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()
