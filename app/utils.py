from datetime import datetime
from uuid import uuid4


def generate_id():
    return str(uuid4())


def generate_datetime():
    return str(datetime.now())