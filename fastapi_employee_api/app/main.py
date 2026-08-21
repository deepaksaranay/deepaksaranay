from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers.employees import router as employee_router
from .users import router as auth_router
from . import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management API",
    version="3.0.0",
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(employee_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "Employee Management API is running"}
