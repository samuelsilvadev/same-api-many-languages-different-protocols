from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from src.db import get_session
from src.routes.schemas import CreateUserPayload, GetUserResponse
from src.config import logging_instance
import traceback
from src.routes.schemas import CreateUserResponse
from src.repository import users_repository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", response_model=GetUserResponse, status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_session)):
    try:
        user = users_repository.get_user_by_id(db, id)

        if user is None:
            logging_instance.info(f"User with {id} does not exist")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        logging_instance.info(f"User with id: {id} found.")

        return GetUserResponse(id=user.id, name=user.name, email=user.email)
    except Exception as error:
        traceback.print_exc()
        logging_instance.error(error)

        if isinstance(error, HTTPException):
            raise error

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED
)
async def save_user(body: CreateUserPayload, db: Session = Depends(get_session)):
    try:
        new_user = users_repository.create_user(db, body)
        logging_instance.info("User is created successfully.")
        return CreateUserResponse(
            id=new_user.id, email=new_user.email, name=new_user.name
        )
    except Exception as error:
        traceback.print_exc()
        logging_instance.error(error)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
