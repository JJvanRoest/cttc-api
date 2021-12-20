from passlib.hash import sha256_crypt
import random
import string

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
