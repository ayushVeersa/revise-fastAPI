from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.role import Role

class EmployeeBase(BaseModel):
    age: int
    designation: str


class EmployeeCreate(EmployeeBase):
    # employee is backed by a User record (unique by user_id)
    user_id: int


class EmployeeRegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    designation: str
    department_id: int
    role: Role
    age: int | None = None

    model_config = ConfigDict(extra="forbid")


class EmployeeUpdate(BaseModel):
    age: int | None = None
    designation: str | None = None
    model_config = {"extra": "forbid"}


class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }