from pydantic import BaseModel


class SuggestionCreate(BaseModel):
    username: str
    title: str
    author: str | None = None


class SuggestionOut(BaseModel):
    id: int
    username: str
    title: str
    author: str | None = None

    model_config = {"from_attributes": True}


class MonthlyPickOut(BaseModel):
    id: int
    month: str
    suggestion: SuggestionOut

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str