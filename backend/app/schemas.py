from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import Perfil


class UsuarioCrear(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    nombre: str = Field(min_length=1, max_length=120)
    perfil: Perfil
    ageb: str | None = Field(default=None, max_length=20)
    acepto_aviso_privacidad: bool


class LoginEntrada(BaseModel):
    email: EmailStr
    password: str


class UsuarioPublico(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    nombre: str
    perfil: Perfil
    ageb: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
