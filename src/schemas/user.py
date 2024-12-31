from pydantic import BaseModel
from pydantic import ConfigDict


class User(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(User):
    id: int

    model_config = ConfigDict(from_attributes=True)
