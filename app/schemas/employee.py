from pydantic import BaseModel


class EmployeeBase(BaseModel):
    age: int
    designation: str


class EmployeeCreate(EmployeeBase):
    user_id: int


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }