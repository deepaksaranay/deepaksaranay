from sqlalchemy.orm import Session

from ..models import Employee


def get_all(db: Session) -> list[Employee]:
    return db.query(Employee).all()


def get_by_id(db: Session, employee_id: int) -> Employee | None:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_by_email(db: Session, email: str) -> Employee | None:
    return db.query(Employee).filter(Employee.email == email).first()


def create(db: Session, employee: Employee) -> Employee:
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def delete(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()
