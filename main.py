from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


# Create the FastAPI application
app = FastAPI()


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    math: float = Field(ge=0, le=10)
    english: float = Field(ge=0, le=10)
    science: float = Field(ge=0, le=10)


class StudentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    math: float = Field(ge=0, le=10)
    english: float = Field(ge=0, le=10)
    science: float = Field(ge=0, le=10)


students = [
    {
        "id": 1,
        "name": "An",
        "average": 8.0,
    },
    {
        "id": 2,
        "name": "Binh",
        "average": 6.17,
    },
    {
        "id": 3,
        "name": "Chi",
        "average": 9.0,
    },
]


@app.get("/")
def read_root():
    return {
        "message": "Student Score API",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found",
    )


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
)
def create_student(student: StudentCreate):
    if students:
        new_id = max(
            student_item["id"]
            for student_item in students
        ) + 1
    else:
        new_id = 1

    print(new_id)

    average = round(
        (
            student.math
            + student.english
            + student.science
        )
        / 3,
        2,
    )

    new_student = {
        "id": new_id,
        "name": student.name,
        "math": student.math,
        "english": student.english,
        "science": student.science,
        "average": average,
    }

    students.append(new_student)
    return new_student


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_data: StudentUpdate,
):
    # Find the student by ID
    for index, student in enumerate(students):
        if student["id"] == student_id:
            # Calculate the updated average
            average = round(
                (
                    updated_data.math
                    + updated_data.english
                    + updated_data.science
                )
                / 3,
                2,
            )

            # Create the updated student
            updated_student = {
                "id": student_id,
                "name": updated_data.name,
                "math": updated_data.math,
                "english": updated_data.english,
                "science": updated_data.science,
                "average": average,
            }

            # Replace the existing student
            students[index] = updated_student

            return updated_student

    raise HTTPException(
        status_code=404,
        detail="Student not found",
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student["id"] == student_id:
            deleted_student = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student": deleted_student,
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
