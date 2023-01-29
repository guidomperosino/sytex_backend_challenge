from datetime import datetime
from fastapi import APIRouter, Body, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import form as schemas
from typing import List, Optional, Any
import logging

router = APIRouter()

@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
def create(
    form_in : schemas.Form
) -> Any:
    return True