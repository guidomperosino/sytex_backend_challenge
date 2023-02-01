from datetime import datetime
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas import form as schemas
from app.models import form as models
from app.utils import to_form_template_out, to_form_instance_out

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
def get_form_template_by_id(db: Session, form_template_id: str): 
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
    
    return query.offset(skip).limit(limit).all()
    # return [to_form_template_out(form_template) for form_template in query.offset(skip).limit(limit).all()]


# Create a new Form Instance.
def create_form_instance(db: Session, form_instance: schemas.FormInstance):
    
    db_form_instance = models.FormInstance(**form_instance.dict(exclude={"answers"}))
    db_form_instance.coordinates = str(db_form_instance.coordinates)

    db.add(db_form_instance)
    db.commit()
    for answer in form_instance.answers:
        db_answer = models.FormResponse(**answer.dict(),form_instance_id=db_form_instance.id)
        db.add(db_answer)
    db.commit()
    db.refresh(db_form_instance)
    return db_form_instance


# Create a new Form Instance.
def create_form_instance_v2(db: Session, form_instance: schemas.FormInstance, db_form_template: schemas.FormTemplateDB):
    
    db_form_instance = models.FormInstance2(**form_instance.dict(exclude={"answers"}))
    db_form_instance.coordinates = str(db_form_instance.coordinates)

    db.add(db_form_instance)
    db.commit()
    
    for item in db_form_template.content:
        if item.type == "group":
            db_response = models.FormResponse2(**item.dict(exclude={"id"}),form_instance_id=db_form_instance.id, form_item_id= item.id)
        else:
            for answer in form_instance.answers:
                if answer.form_item_id == item.id:
                    db_response = models.FormResponse2(**item.dict(exclude={"id","options"}),form_instance_id=db_form_instance.id, form_item_id= item.id, answer=answer.answer)
        db.add(db_response)
    db.commit()
    db.refresh(db_form_instance)
    return db_form_instance

# Return Form Template List from DB (filtered case insensitive).
def get_form_instances(db: Session, skip=0, limit=100):
    query = db.query(models.FormInstance)
    # return query.offset(skip).limit(limit).all()
    return [to_form_instance_out(form_instance) for form_instance in query.offset(skip).limit(limit).all()]
