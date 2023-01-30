from datetime import datetime
from fastapi import APIRouter, Body, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import form as schemas
from app.crud import form as crud
from typing import List, Optional, Any
import logging

router = APIRouter()

@router.post("", response_model=schemas.FormTemplateDB, status_code=status.HTTP_201_CREATED)
def create(
    form_in : schemas.FormTemplate,
    db: Session = Depends(deps.get_db),
):
    return crud.create_form_template(db=db, form_template=form_in)