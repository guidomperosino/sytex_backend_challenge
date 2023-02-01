
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
        return to_form_group_out(form_item)
    else:
        if form_item.input_type == 1:
            return to_form_text_entry_out(form_item)
        elif form_item.input_type == 2:
            options = [to_entry_option_out(option) for option in form_item.options]
            return to_form_options_entry_out(form_item, options)
        elif form_item.input_type == 3:
            return to_form_yes_no_entry_out(form_item)


def to_entry_option_out(entry_option):
    return schemas.OptionOut(
        id=entry_option.id,
        label=entry_option.label,
        value=entry_option.value,
        is_active=entry_option.is_active,
        created_at=entry_option.created_at
    )

def to_form_group_out(group_item):
    return schemas.FormGroupOut(
        id=group_item.id,
        index=group_item.index,
        type=group_item.type,
        name=group_item.name,
        is_active=group_item.is_active,
        created_at=group_item.created_at,
    )

def to_form_options_entry_out(options_entry_item, options):
    return schemas.FormOptionsEntryOut(
        id=options_entry_item.id,
        index=options_entry_item.index,
        type=options_entry_item.type,
        label=options_entry_item.label,
        input_type=options_entry_item.input_type,
        is_active=options_entry_item.is_active,
        created_at=options_entry_item.created_at,
        options=options
    )

def to_form_text_entry_out(text_entry_item):
            return schemas.FormTextEntryOut(
                id=text_entry_item.id,
                index=text_entry_item.index,
                type=text_entry_item.type,
                label=text_entry_item.label,
                input_type=text_entry_item.input_type,
                is_active=text_entry_item.is_active,
                created_at=text_entry_item.created_at,
            )

def to_form_yes_no_entry_out(yes_no_entry_item):
            return schemas.FormYesNoEntryOut(
                id=yes_no_entry_item.id,
                index=yes_no_entry_item.index,
                type=yes_no_entry_item.type,
                label=yes_no_entry_item.label,
                input_type=yes_no_entry_item.input_type,
                is_active=yes_no_entry_item.is_active,
                created_at=yes_no_entry_item.created_at,
            )