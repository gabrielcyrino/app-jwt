import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Em produção, a variável de ambiente DATABASE_URL é definida
# pelo Render automaticamente, apontando para o PostgreSQL.
#DATABASE_URL = os.getenv("DATABASE_URL")

# --- TESTE LOCAL COM SQLITE (opcional) -----------------------
# Se quiser testar SEM instalar o PostgreSQL, comente a linha
# acima (ou deixe DATABASE_URL vazia no .env) e descomente a
# linha abaixo: o SQLite cria um arquivo 'app.db' na pasta do
# projeto, sem precisar de servidor de banco algum.
DATABASE_URL = "sqlite:///./app.db"

# Rede de segurança: se nenhuma DATABASE_URL foi definida, cai
# automaticamente no SQLite, para o app não quebrar localmente.
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./app.db"

# O Render entrega a URL começando com "postgres://", mas o
# SQLAlchemy moderno espera "postgresql://". Esta linha ajusta.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 'check_same_thread' é um argumento exclusivo do SQLite.
# Só o aplicamos quando a URL for de SQLite, para não quebrar
# a conexão com o PostgreSQL.
connect_args = (
    {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependência do FastAPI: abre uma sessão do banco para cada requisição
    e fecha automaticamente quando a requisição termina."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()