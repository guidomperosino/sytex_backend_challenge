from typing import Optional, Tuple, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Options(BaseModel):
    label: str = Field(...)
    value: str =  Field (...)

class BaseItem(BaseModel):
    index: str = Field(...)
    type: str = Field(...)

class Entry(BaseItem):
    input_type: int = Field(...)
    label: str = Field(...)

class Group(BaseItem):
    name:str = Field(...)

class OptionsEntry(Entry):
    options: list[Options] = Field(...)
    
    @validator("input_type")
    def type_validation(cls, input_type):
        if input_type != 2:
            raise ValueError("Not an Options Entry")
        return input_type
    
    @validator("options")
    def options_validation(cls, options):
        if len(options) < 2:
            raise ValueError("Required at least 2 options")
        return options

class TextInputEntry(Entry):
    
    @validator("input_type")
    def type_validation(cls, input_type):
        if input_type != 1:
            raise ValueError("Not a Text Input Entry")
        return input_type

class YesNoEntry(Entry):
    
    @validator("input_type")
    def type_validation(cls, input_type):
        if input_type != 3:
            raise ValueError("Not a Yes/No Entry")
        return input_type

class FormTemplate(BaseModel):
    name: str = Field(...)
    description: str =  Field (...)
    content : list[Union[Group,TextInputEntry,OptionsEntry,YesNoEntry]] = Field(...)
    # coordinates: Tuple[float, float] = Field(...)


class FormTemplateDB(FormTemplate):
    id: str
    created_at: datetime
    content : list
    class Config:
        orm_mode = True


class EntryOptionOut(BaseModel):
    id: str
    label: str
    value: str
    is_active: bool
    created_at: datetime


class FormItemOut(BaseModel):
    id: str
    index: str
    type: str
    name: Optional[str]
    label: Optional[str]
    input_type: Optional[int]
    is_active: bool
    created_at: datetime
    options: list[EntryOptionOut]

class FormTemplateOut(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
    content: list[FormItemOut]
