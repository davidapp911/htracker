from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import auth, habits, stats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://htracker-tau.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(habits.router, prefix="/habits", tags=["habits"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/health")
def status():
    return {"status": "ok"}
