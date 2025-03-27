from src.security import check_api_key, get_api_key_hash
from fastapi import HTTPException, status


def validate_api_key(api_key: str):
    if not check_api_key(api_key, get_api_key_hash()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
