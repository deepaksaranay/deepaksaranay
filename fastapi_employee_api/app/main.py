from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .dependencies import get_current_user
from .models import Employee
from .schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from .users import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API", version="2.0.0")
app.include_router(auth_router)


@app.get("/")
def health_check():
    return {"message": "Employee Management API is running"}


@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return db.query(Employee).all()


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing = db.query(Employee).filter(Employee.id == employee_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")

    duplicate = db.query(Employee).filter(
        Employee.email == employee.email,
        Employee.id != employee_id,
    ).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Email already registered")

    for key, value in employee.model_dump().items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
