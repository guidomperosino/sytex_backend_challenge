from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())


def generate_datetime():
    return str(datetime.now())

 
class FormTemplate(Base):
    __tablename__ = "form_templates"
    id = Column(String(36), primary_key=True, default=generate_id ,index=True)
    name = Column(String(100))
    description = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=generate_datetime)

    content = relationship("FormItem")

class FormItem(Base):
    __tablename__ = "form_items"
    id = Column(String(36), primary_key=True, default=generate_id ,index=True)
    form_template_id = Column(String(36),ForeignKey("form_templates.id"))
    index = Column(String(15))
    type = Column(String(30))
    name = Column(String(250))
    label = Column(String(250))
    input_type = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=generate_datetime)

    options = relationship("EntryOption")

class EntryOption(Base):
    __tablename__ = "entry_options"
    id = Column(String(36), primary_key=True, default=generate_id ,index=True)
    form_item_id = Column(String(36),ForeignKey("form_items.id"))
    label = Column(String(250))
    value = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=generate_datetime)

