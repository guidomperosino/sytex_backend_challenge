from datetime import datetime
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas import form as schemas
from app.models import form as models
from app.utils import to_form_template_out

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


# Create a new Template.
def create_form_template(db: Session, form_template: schemas.FormTemplate):
    db_form_template = models.FormTemplate(**form_template.dict(exclude={"content"}))

    with db.begin():
        db.add(db_form_template)
        db.flush()
        for item in form_template.content:
            db_form_item = models.FormItem(**item.dict(exclude={"options"}),form_template_id=db_form_template.id)
            db.add(db_form_item)
            db.flush()
            if isinstance(item, schemas.OptionsEntry):
                for option in item.options:
                    db_entry_option = models.EntryOption(**option.dict(),form_item_id=db_form_item.id)
                    db.add(db_entry_option)
                    db.flush()
        db.commit()
        db.refresh(db_form_template)
    return db_form_template

# Return Form Template from DB (based on id).
def get_form_template(db: Session, form_template_id: str): 
    form_template = db.query(models.FormTemplate).filter(models.FormTemplate.id == form_template_id).first()

    return to_form_template_out(form_template)

# Return Form Template List from DB (filtered case insensitive).
def get_form_templates(db: Session, skip=0, limit=100, name=None, description=None):
    query = db.query(models.FormTemplate)

    filters = []

    if name:
        filters.append(models.FormTemplate.name.ilike(f"%{name}%"))
    if description:
        filters.append(models.FormTemplate.description.ilike(f"%{description}%"))

    if filters:
        query = query.filter(and_(*filters))
    
    return [to_form_template_out(form_template) for form_template in query.offset(skip).limit(limit).all()]