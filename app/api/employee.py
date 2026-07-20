from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.core.permissions import require_roles
from app.core.role import Role
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeRegistrationRequest,
)
from app.services.employee import (
    get_employee,
    get_employees,
    create_employee,
    update_employee,
    delete_employee,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.get(
    "",
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_roles(Role.ADMIN, Role.MANAGER))],
)
def get_all_employees(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_employees(db, skip, limit)


@router.get("/{employee_id}",response_model=EmployeeResponse)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_employee(db, employee_id)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.ADMIN))],
)
def create_new_employee(
    payload: EmployeeRegistrationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Create User first, then Employee profile
    return create_employee(db, payload)


@router.put(
    "{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(require_roles(Role.ADMIN, Role.MANAGER))],
)
def update_existing_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_employee(
        db,
        employee_id,
        employee,
    )



@router.delete(
    "{employee_id}",
    dependencies=[Depends(require_roles(Role.ADMIN))],
)
def delete_existing_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_employee(
        db,
        employee_id,
    )
