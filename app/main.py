from fastapi import FastAPI
from app.api.auth import router

app = FastAPI()

app.include_router(router)

@app.get("/health")
def check_health():
    return {"health": "ok"}


