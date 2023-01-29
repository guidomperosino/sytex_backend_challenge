from typing import Optional, Tuple
from pydantic import BaseModel, Field, EmailStr
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

class TextInputEntry(Entry):
    pass

class YesNoEntry(Entry):
    pass

class Form(BaseModel):
    name: str = Field(...)
    description: str =  Field (...)
    created_at : datetime = Field(...)
    content : list[BaseItem] = Field(...)
    coordinates: Tuple[float, float] = Field(...)
