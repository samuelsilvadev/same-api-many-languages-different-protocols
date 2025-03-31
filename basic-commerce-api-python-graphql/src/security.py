from src.config import config_instance
from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def build_password_hash(password: str) -> str:
    return pass_context.hash(password)


def check_api_key(api_key, api_hash) -> bool:
    return pass_context.verify(api_key, api_hash)


def build_api_key_hash(api_key: str) -> str:
    return pass_context.hash(api_key)


def get_api_key_hash() -> str:
    return build_api_key_hash(config_instance.API_KEY)
