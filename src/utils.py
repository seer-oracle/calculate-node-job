"""
   Description:
        -
        -
"""
import string
from datetime import timezone, datetime
from random import choice

from bson import ObjectId


def get_current_time():
    return datetime.utcnow()


def dt_utcnow():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def is_oid(oid: str) -> bool:
    return ObjectId.is_valid(oid)


def random_str(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(choice(chars) for x in range(size))
