from fastapi import FastAPI

app = FastAPI(
    title="Consulta Livros API",
    version="1.0.0",
    description="API de consulta de biblioteca de livros."
)

@app.get("/")
async def home():
    return "Hello, FastAPI" 