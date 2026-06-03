from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """O que o cliente envia para registrar um usuário."""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """O que o backend devolve sobre um usuário. Note que NÃO inclui senha."""
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # permite criar a partir de um objeto SQLAlchemy


class Token(BaseModel):
    """Resposta do endpoint de login."""
    access_token: str
    token_type: str = "bearer"