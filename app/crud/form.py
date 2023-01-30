from datetime import datetime
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas import form as schemas
from app.models import form as models


from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder



# Create a new Template.
def create_form_template(db: Session, form_template: schemas.FormTemplate):
    db_form_template = models.FormTemplate(**form_template.dict(exclude={"content"}))

    with db.begin_nested():
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
        db.refresh(db_form_template)

    return db_form_template
