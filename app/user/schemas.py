from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


EXAMPLE_ID = ObjectId()


class UserSchema(BaseModel):
    """
    Mongodb add 'id' by default
    """

    name: str
    admin: bool = False

    class Config:
        schema_extra = {
            "example": {"id": f"{EXAMPLE_ID}", "name": "joseph", "admin": False}
        }


class UserSchemaCreate(UserSchema):
    class Config:
        schema_extra = {"example": {"name": "joseph", "admin": False}}


class UserSchemaUpdate(BaseModel):
    name: Optional[str]
    admin: Optional[bool]

    class Config:
        schema_extra = {"example": {"name": "joseph", "admin": False}}


class UserSchemaDelete(BaseModel):
    detail: str

    class Config:
        schema_extra = {"example": {"detail": f"User {EXAMPLE_ID} deleted"}}
