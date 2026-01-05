from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="Books_API",
    version="1.0.0",
    description="API de consulta de biblioteca de livros."
)

app.include_router(api_v1_router, prefix="/api/v1")
