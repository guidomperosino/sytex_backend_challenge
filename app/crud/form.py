from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.schemas import form as schemas
from app.models import form as models


# Create a new Template.
def create_form_template(db: Session, form_template: schemas.FormTemplate):
    db_form_template = models.FormTemplate(**form_template.dict(exclude={"content"}))
    
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
    db_form_template = db.query(models.FormTemplate).filter(models.FormTemplate.id == form_template_id).first()
    return db_form_template

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

# Create a new Form Instance.
def create_form_instance(
    db: Session,
    form_instance: schemas.FormInstance,
    db_form_template: schemas.FormTemplateOut
    ):
    
    db_form_instance = models.FormInstance(**form_instance.dict(exclude={"answers"}))
    db_form_instance.coordinates = str(db_form_instance.coordinates)
    
    db.add(db_form_instance)
    db.flush()
    
    for item in db_form_template.content:
        if item.type == "group":
            db_response = models.FormResponse(
                index = item.index,
                type = item.type,
                name = item.name,
                form_instance_id=db_form_instance.id,
                form_item_id= item.id
            )
            db.add(db_response)
            db.flush()
            continue
        else:
            for answer in form_instance.answers:
                if answer.form_item_id == item.id:
                    db_response = models.FormResponse(
                        index = item.index,
                        type = item.type,
                        label = item.label,
                        input_type = item.input_type,
                        form_instance_id=db_form_instance.id,
                        form_item_id= item.id,
                        answer=answer.answer
                    )
                    db.add(db_response)
                    db.flush()
                    break
            continue
    db.commit()
    db.refresh(db_form_instance)
    return db_form_instance

# Return Form Instances List from DB (filtered case insensitive).
def get_form_instances(db: Session, skip=0, limit=100):
    query = db.query(models.FormInstance)
    return query.offset(skip).limit(limit).all()
