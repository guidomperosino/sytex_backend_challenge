from fastapi import APIRouter,HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas import form as schemas
from app.crud import form as crud


router = APIRouter()

@router.post("", response_model=schemas.FormInstanceOut, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
def create(
    form_instance : schemas.FormInstance,
    db: Session = Depends(deps.get_db),
):
    db_form_template = crud.get_form_template_by_id(db, form_template_id= form_instance.form_template_id)
    
    if db_form_template is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form Template not found")

    answers_items_id = [answer.form_item_id for answer in form_instance.answers]
    items_in_form = [item.id for item in db_form_template.content if item.type =="entry"]
    
    if set(answers_items_id) != set(items_in_form) or len(set(answers_items_id)) != len(answers_items_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answers input does not Match with the Form Template")

    for item in db_form_template.content:
        if item.type == "entry":
            for answer in form_instance.answers:
                if answer.form_item_id == item.id:
                    if item.input_type == 1:
                        if not isinstance(answer.answer,str):
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answers input does not Match with Text input format")
                        continue
                    elif item.input_type == 2:
                        if not isinstance(answer.answer,str) or answer.answer not in [option.value for option in item.options]:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answers input does not Match with Option input format")
                        continue
                    elif item.input_type ==3:
                        if not isinstance(bool(answer.answer),bool):
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answers input does not Match with Yes/NO input format")
                        continue
    return crud.create_form_instance(db=db, form_instance=form_instance, db_form_template=db_form_template)


@router.get("",response_model=list[schemas.FormInstanceOut], response_model_exclude_none=True)
def get_all(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    return crud.get_form_instances(
        db=db, 
        skip=skip, 
        limit=limit
    )