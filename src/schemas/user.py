from pydantic import BaseModel


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserRead(User):
    id: int

    class Config:
        orm_mode = True
