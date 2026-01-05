from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="Books_API",
    version="1.0.0",
    description="API de consulta de biblioteca de livros."
)

# Inclue um informativo na rota principal
@app.get("/api/v1", tags=["Info"])
def api_v1_root():
    return {
        "name": "Books API",
        "version": "v1",
        "docs": "/docs"
    }

app.include_router(api_v1_router, prefix="/api/v1")
