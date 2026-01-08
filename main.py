from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.v1.router import router as api_v1_router
from app.db.session import engine
from app.models import auth
from sqlmodel import SQLModel

app = FastAPI(
    title="Books_API",
    version="1.0.0",
    description="API de consulta de biblioteca de livros.",
    swagger_ui_parameters={
        'persistAuthorization': True
    }
)
security = HTTPBearer()

# Inclue um informativo na rota principal
@app.get("/api/v1", tags=["Info"])
def api_v1_root():
    return {
        "name": "Books API",
        "version": "v1",
        "docs": "/docs"
    }

app.include_router(api_v1_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
