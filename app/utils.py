
import os
import re
import time
from datetime import datetime, timedelta
from typing import Union, Any
# from jose import jwt
# from passlib.context import CryptContext
from app.core.config import settings
import logging

logger = logging.getLogger()

# JWT
ALGORITHM = "HS256"

# HASH PASSWORD
# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None):
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode = {"exp": expire, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    
#     return encoded_jwt


# def get_hashed_password(password: str):
#     return password_context.hash(password)


# def verify_password(password: str, hashed_pass: str):
#     return password_context.verify(password, hashed_pass)


def normalize_filename(filename):
    name, file_ext = os.path.splitext(filename)
    file_name_modify = re.sub('[\s]+', '_', name).lower() 
    timestamp = str(int(time.time()))
    object_name = file_name_modify + '_' + timestamp + file_ext

    return object_name