from datetime import datetime, timedelta
import jwt
from passlib.hash import sha256_crypt
import random
import string
from config import CONFIG
from ...database.users import Users
from typing import Optional, Dict
from quart import Request
from ...database.company import Company


def get_random_string() -> str:
    chars = string.ascii_letters + string.punctuation
    size = 12
    return ''.join(random.choice(chars) for _ in range(size))


def hash_api_key(api_key: str) -> str:
    return sha256_crypt.hash(api_key)


def verify_api_key(company: Company, api_key: str) -> bool:
    return sha256_crypt.verify(api_key, company.api_key)


def check_auth(type: str) -> bool:
    return True


async def create_jwt_token(user: Dict) -> str:
    enc_jwt = jwt.encode({
        "id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "company": user['company']['id'],
        "exp": datetime.utcnow() + timedelta(hours=2),
        "iat": datetime.utcnow()
    }, CONFIG.auth["jwt_secret_key"], algorithm="HS256")
    return enc_jwt


async def get_auth_token(req: Request) -> Optional[Dict]:
    auth_header = await req.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    try:
        dec_jwt = jwt.decode(auth_token, CONFIG.auth["jwt_secret_key"], algorithms=[
                             "HS256"], options={"require_exp": True})
    except (jwt.exceptions.DecodeError, jwt.InvalidTokenError):
        return None
    return dec_jwt
