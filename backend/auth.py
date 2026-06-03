import os
from datetime import datetime, timedelta, timezone

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import get_db
from models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não definida no .env")

# Esquema que extrai o token do header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# O bcrypt só processa os primeiros 72 BYTES da senha. Versões
# recentes (>= 5.0) lançam erro se a senha for maior, em vez de
# truncar silenciosamente. Por isso truncamos aqui, de forma
# explícita, antes de gerar/verificar o hash.
def _to_72_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    hashed = bcrypt.hashpw(_to_72_bytes(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica se uma senha em texto puro corresponde ao hash."""
    return bcrypt.checkpw(_to_72_bytes(plain), hashed.encode("utf-8"))


def create_access_token(data: dict) -> str:
    """Gera um JWT assinado com os dados informados + expiração."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Dependência que valida o JWT e retorna o usuário correspondente.

    Usada em rotas protegidas: basta declarar
    `current_user: User = Depends(get_current_user)`.
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exc
    except JWTError:
        # Inclui: assinatura inválida, token expirado, formato inválido
        raise credentials_exc

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exc
    return user