from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def build_password_hash(password: str) -> str:
    return pass_context.hash(password)
