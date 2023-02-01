from fastapi import APIRouter,HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import form as schemas
from app.crud import form as crud
from typing import Optional

router = APIRouter()

@router.post("", response_model=schemas.FormTemplateDB, status_code=status.HTTP_201_CREATED)
def create(
    form_in : schemas.FormTemplate,
    db: Session = Depends(deps.get_db),
):
    return crud.create_form_template(db=db, form_template=form_in)


@router.get("/{form_template_id}", response_model=schemas.FormTemplateOut)
def get_by_id(
    form_template_id: str, 
    db: Session = Depends(deps.get_db),
):
    db_form_template = crud.get_form_template_by_id(db, form_template_id= form_template_id)
    
    if db_form_template is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form Template not found")
    
    return db_form_template


@router.get("", response_model=list[schemas.FormTemplateOut], response_model_exclude_none=True)
def get_all(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(deps.get_db),
):
    return crud.get_form_templates(
        db=db, 
        skip=skip, 
        limit=limit, 
        name=name, 
        description=description
    )