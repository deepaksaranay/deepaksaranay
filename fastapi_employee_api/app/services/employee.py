from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import Employee
from ..repositories import employee as repository
from ..schemas import EmployeeCreate, EmployeeUpdate


def list_employees(db: Session):
    return repository.get_all(db)


def get_employee(db: Session, employee_id: int):
    employee = repository.get_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def create_employee(db: Session, data: EmployeeCreate):
    if repository.get_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    employee = Employee(**data.model_dump())
    return repository.create(db, employee)


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate):
    employee = get_employee(db, employee_id)
    duplicate = repository.get_by_email(db, data.email)
    if duplicate and duplicate.id != employee_id:
        raise HTTPException(status_code=409, detail="Email already registered")
    for key, value in data.model_dump().items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    repository.delete(db, employee)
    return {"message": "Employee deleted successfully"}
