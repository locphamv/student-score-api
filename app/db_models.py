from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    __tablename__ = "students"  

    id: int | None = Field(
        default=None,
        primary_key=True,
    )
    name: str = Field(index=True)
    math: float
    english: float
    science: float
    average: float


