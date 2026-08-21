from fastapi import FastAPI

from .routers.employees import router as employee_router
from .users import router as auth_router

app = FastAPI(title="Employee Management API", version="3.0.0")
app.include_router(auth_router)
app.include_router(employee_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "Employee Management API is running"}
