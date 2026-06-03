import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import router

load_dotenv()

# Cria as tabelas no banco se ainda não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab JWT API")

# Origens permitidas no CORS.
# Em produção, defina ALLOWED_ORIGINS no Render com a URL do
# frontend na Vercel (várias URLs separadas por vírgula).
# Ex.: ALLOWED_ORIGINS=https://meu-app.vercel.app
# Sem a variável, usa o frontend local (Vite em :5173).
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
origins = [o.strip() for o in origins if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "API de Autenticação JWT rodando"}