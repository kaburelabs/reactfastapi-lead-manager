import datetime as _dt
from pydantic import BaseModel
from typing import Optional


class _UserBase(BaseModel):
    email: Optional[str]


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: Optional[int]
    class Config:
        orm_mode = True
        
class _LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str


class LeadCreate(_LeadBase):
    pass


class Lead(_LeadBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_update: _dt.datetime

    class Config:
        orm_mode = True