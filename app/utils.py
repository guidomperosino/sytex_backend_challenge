
import os
import re
import time
from datetime import datetime, timedelta
from typing import Union, Any
# from jose import jwt
# from passlib.context import CryptContext
from app.core.config import settings
import logging
from uuid import uuid4
from datetime import datetime
from app.schemas import form as schemas

logger = logging.getLogger()

# JWT
ALGORITHM = "HS256"

def generate_id():
    return str(uuid4())


def generate_datetime():
    return str(datetime.now())

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

def to_form_instance_out(form_instance):
    form_template = to_form_template_out(form_instance.form_template)
    return schemas.FormInstanceOut(
        id=form_instance.id,
        form_template_id=form_instance.form_template_id,
        coordinates=form_instance.coordinates,
        answers=form_instance.answers,
        form_template=form_template
    )


def to_form_template_out(form_template):
    content = [to_form_item_out(item) for item in form_template.content]
    return schemas.FormTemplateOut(
        id=form_template.id,
        name=form_template.name,
        description=form_template.description,
        is_active=form_template.is_active,
        created_at=form_template.created_at,
        content=content
    )

def to_form_item_out(form_item):
    if form_item.type == "group":
        return schemas.FormGroupOut(
            id=form_item.id,
            index=form_item.index,
            type=form_item.type,
            name=form_item.name,
            is_active=form_item.is_active,
            created_at=form_item.created_at,
        )
    else:
        if form_item.input_type == 2:
            options = [to_entry_option_out(option) for option in form_item.options]
            return schemas.FormOptionsEntryOut(
                id=form_item.id,
                index=form_item.index,
                type=form_item.type,
                label=form_item.label,
                input_type=form_item.input_type,
                is_active=form_item.is_active,
                created_at=form_item.created_at,
                options=options
            )
        elif form_item.input_type == 1:
            return schemas.FormTextEntryOut(
                id=form_item.id,
                index=form_item.index,
                type=form_item.type,
                label=form_item.label,
                input_type=form_item.input_type,
                is_active=form_item.is_active,
                created_at=form_item.created_at,
            )
        elif form_item.input_type == 3:
            return schemas.FormYesNoEntryOut(
                id=form_item.id,
                index=form_item.index,
                type=form_item.type,
                label=form_item.label,
                input_type=form_item.input_type,
                is_active=form_item.is_active,
                created_at=form_item.created_at,
            )


def to_entry_option_out(entry_option):
    return schemas.EntryOptionOut(
        id=entry_option.id,
        label=entry_option.label,
        value=entry_option.value,
        is_active=entry_option.is_active,
        created_at=entry_option.created_at
    )