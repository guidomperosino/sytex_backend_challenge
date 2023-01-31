from typing import Optional, Tuple, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Option(BaseModel):
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


class TextInputEntry(Entry):
    
    # Validate input_type = 1 => TexttEntry.
    @validator("input_type")
    def type_validation(cls, input_type):
        if input_type != 1:
            raise ValueError("Not a Text Input Entry")
        return input_type


class OptionsEntry(Entry):
    options: list[Option] = Field(...)
    
    # Validate input_type = 2 => OptionsEntry.
    @validator("input_type")
    def type_validation(cls, input_type):
        if input_type != 2:
            raise ValueError("Not an Options Entry")
        return input_type
    
    # Validate OptionsEntry with at least 2 options.
    @validator("options")
    def options_validation(cls, options):
        if len(options) < 2:
            raise ValueError("Required at least 2 options")
        return options


class YesNoEntry(Entry):

    # Validate input_type = 3 => YES/NO Entry.    
    @validator("input_type")
    def type_validation(cls, input_type):
        if input_type != 3:
            raise ValueError("Not a Yes/No Entry")
        return input_type

class FormTemplate(BaseModel):
    name: str = Field(...)
    description: str =  Field (...)
    content : list[Union[Group,TextInputEntry,OptionsEntry,YesNoEntry]] = Field(...)


class FormTemplateDB(FormTemplate):
    id: str
    created_at: datetime
    content : list
    class Config:
        orm_mode = True


class OptionOut(BaseModel):
    id: str
    label: str
    value: str
    is_active: bool
    created_at: datetime

class FormGroupOut(BaseModel):
    id: str
    index: str
    type: str
    name: str
    is_active: bool
    created_at: datetime

class FormOptionsEntryOut(BaseModel):
    id: str
    index: str
    type: str
    label: str
    input_type: int
    is_active: bool
    created_at: datetime
    options: list[OptionOut]

class FormTextEntryOut(BaseModel):
    id: str
    index: str
    type: str
    label: str
    input_type: int
    is_active: bool
    created_at: datetime

class FormYesNoEntryOut(BaseModel):
    id: str
    index: str
    type: str
    label: str
    input_type: int
    is_active: bool
    created_at: datetime
class FormTemplateOut(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
    content: list[Union[FormGroupOut,FormOptionsEntryOut,FormTextEntryOut,FormYesNoEntryOut]]

class FormAnswer(BaseModel):
    form_item_id:str
    answer: Union[str,int, bool]

class FormInstance(BaseModel):
    form_template_id : str
    coordinates: Tuple[float, float]
    answers : list[FormAnswer]
    
    @validator("coordinates")
    def validate_coordinates(cls, coordinates):
        if not (-90 <= coordinates[0] <= 90) or not (-180 <= coordinates[1] <= 180):
            raise ValueError("Coordinates are out of range")
        return coordinates

class FormInstanceOut(BaseModel):
    id: str
    form_template_id: str
    coordinates: str
    form_template: FormTemplateOut
    answers: list