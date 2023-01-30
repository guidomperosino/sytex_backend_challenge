from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from app.utils import generate_datetime, generate_id
 
class FormTemplate(Base):
    __tablename__ = "form_templates"

    id = Column(String(36), primary_key=True, default=generate_id ,index=True)
    name = Column(String(100))
    description = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=generate_datetime)

    content = relationship("FormItem", order_by="FormItem.index")


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
    form_responses = relationship("FormResponse", back_populates="questions")



class EntryOption(Base):
    __tablename__ = "entry_options"

    id = Column(String(36), primary_key=True, default=generate_id ,index=True)
    form_item_id = Column(String(36),ForeignKey("form_items.id"))
    label = Column(String(250))
    value = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=generate_datetime)


class FormInstance(Base):
    __tablename__ = "form_instances"

    id = Column(String(36), primary_key=True, default=generate_id ,index=True)
    form_template_id = Column(String(36),ForeignKey("form_templates.id"))
    coordinates = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=generate_datetime)

    form = relationship("FormTemplate")

class FormResponse(Base):
    __tablename__ = "form_responses"

    id = Column(Integer, primary_key=True, index=True)
    form_instance_id = Column(String(36), ForeignKey("form_instances.id"))
    form_item_id = Column(String(36), ForeignKey("form_items.id"))
    answer = Column(String(250))
    questions = relationship("FormItem", back_populates="form_responses")
