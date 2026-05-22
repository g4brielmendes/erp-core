from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user
from app.routers import auth

from app.routers import module

from app.routers import health

from fastapi.middleware.cors import CORSMiddleware
from app.routers import users


app = FastAPI(title="Core ERP - G0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

app.include_router(module.router)

app.include_router(health.router)

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"msg": "Core ERP rodando"}

