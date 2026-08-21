from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from ..services import employee as service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=list[EmployeeResponse], dependencies=[Depends(get_current_user)])
def list_employees(db: Session = Depends(get_db)):
    return service.list_employees(db)


@router.get("/{employee_id}", response_model=EmployeeResponse, dependencies=[Depends(get_current_user)])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return service.get_employee(db, employee_id)


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    return service.create_employee(db, data)


@router.put("/{employee_id}", response_model=EmployeeResponse, dependencies=[Depends(get_current_user)])
def update_employee(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    return service.update_employee(db, employee_id, data)


@router.delete("/{employee_id}", dependencies=[Depends(get_current_user)])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    return service.delete_employee(db, employee_id)
