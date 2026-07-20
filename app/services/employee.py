from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import (
    EmployeeUpdate,
    EmployeeRegistrationRequest,
)
from app.schemas.user import UserCreate
from app.services.user_service import create_user


def get_employee(db: Session, employee_id: int) -> Employee:

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


def get_employees(db: Session, skip: int = 0, limit: int = 10):

    return (
        db.query(Employee)
        .filter(Employee.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_employee(
    db: Session,
    payload: EmployeeRegistrationRequest,
) -> Employee:


    # Find/create the backing User
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_user is None:
        user = create_user(
            db,
            UserCreate(
                name=payload.name,
                email=payload.email,
                password=payload.password,
            ),
        )

    employee = (
        db.query(Employee)
        .filter(Employee.user_id == user.id)
        .first()
    )

    if employee:
        employee.age = payload.age or employee.age or 0
        employee.designation = payload.designation
        employee.is_active = True
        db.commit()
        db.refresh(employee)
        return employee

    employee = Employee(
        user_id=user.id,
        age=payload.age or 0,
        designation=payload.designation,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee



def update_employee(
    db: Session,
    employee_id: int,
    employee_update: EmployeeUpdate,
) -> Employee:

    employee = get_employee(db, employee_id)

    update_data = employee_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee_id: int):

    employee = get_employee(db, employee_id)

    employee.is_active = False

    db.commit()

    return {
        "message": "Employee deleted successfully"
    }