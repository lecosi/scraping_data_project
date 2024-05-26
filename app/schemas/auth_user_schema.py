from passlib.context import CryptContext
from pydantic import BaseModel


class InputSigUpModel(BaseModel):
    username: str
    password: str


class InputTokenModel(BaseModel):
    username: str
    password: str


class OutTokenModel(BaseModel):
    access_token: str
    refresh_token: str
    expires: int


class InputRefreshModel(BaseModel):
    refresh_token: str


class CreateUserModel(BaseModel):
    username: str
    password: str

    def get_password_hash(self):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(self.password)
