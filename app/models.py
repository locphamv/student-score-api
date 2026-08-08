from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    math: float = Field(ge=0, le=10)
    english: float = Field(ge=0, le=10)
    science: float = Field(ge=0, le=10)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(BaseModel):
    id: int
    name: str
    math: float
    english: float
    science: float
    average: float


class StudentListResponse(BaseModel):
    total: int
    offset: int
    limit: int
    count: int
    students: list[StudentResponse]


class DeleteStudentResponse(BaseModel):
    message: str
    student: StudentResponse


class StudentPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    math: float | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    english: float | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    science: float | None = Field(
        default=None,
        ge=0,
        le=10,
    )
