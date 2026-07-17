from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int) -> Employee:

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return employee


def get_employees(db: Session, skip: int = 0, limit: int = 10):

    return (
        db.query(Employee)
        .filter(Employee.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_employee(db: Session, employee: EmployeeCreate) -> Employee:

    existing = (
        db.query(Employee)
        .filter(Employee.user_id == employee.user_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee already exists for this user"
        )

    db_employee = Employee(
        user_id=employee.user_id,
        age=employee.age,
        designation=employee.designation,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee



def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate) -> Employee:

    employee = get_employee(db, employee_id)

    # employee.age = employee_update.age
    # employee.designation = employee_update.designation
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