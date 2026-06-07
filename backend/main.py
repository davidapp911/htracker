from fastapi import FastAPI

from backend.api import auth, habits

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(habits.router, prefix="/habits", tags=["habits"])


@app.get("/health")
def status():
    return {"status": "ok"}
