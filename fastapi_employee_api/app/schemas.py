from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(min_length=2, max_length=100)
    salary: int = Field(gt=0)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
