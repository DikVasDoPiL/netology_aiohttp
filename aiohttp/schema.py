from typing import Optional

from pydantic import BaseModel


class CreateAdvert(BaseModel):
    title: str
    description: str
    owner: str


class UpdateAdvert(BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]
