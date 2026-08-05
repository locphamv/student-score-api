from typing import Literal

from dns import query
from fastapi import APIRouter, HTTPException, Query, status

from app.data import students
from app.models import (
    DeleteStudentResponse,
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)

router = APIRouter(
    prefix="/students",
    tags=["students"],
)


@router.get(
    "",
    response_model=StudentListResponse,
)
def get_students(
    passed: bool | None = None,
    minimum_average: float | None = Query(
        default=None,
        ge=0,
        le=10,
    ),
    sort_order: Literal["asc", "desc"] | None = None,
    offset: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
):
    result = students.copy()

    # Filter by pass/fail status
    if passed is not None:
        if passed:
            result = [
                student
                for student in result
                if student["average"] >= 5
            ]
        else:
            result = [
                student
                for student in result
                if student["average"] < 5
            ]

        # Filter by minimum average score
    if minimum_average is not None:
        result = [
            student
            for student in result
            if student["average"] >= minimum_average
        ]

        # Sort by average score
    if sort_order is not None:
        result.sort(
            key=lambda student: student["average"],
            reverse=sort_order == "desc",
        )

        # Count before pagination
    total = len(result)

    # Apply pagination
    paginated_students = result[offset: offset + limit]

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(paginated_students),
        "students": paginated_students,
    }


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found",
    )


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(student: StudentCreate):
    if student:
        new_id = max(
            student_item["id"]
            for student_item in students
        ) + 1
    else:
        new_id = 1

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


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_id: int,
    updated_data: StudentUpdate,
):
    for index, student in enumerate(students):
        if student["id"] == student_id:
            average = round(
                (
                    updated_data.math
                    + updated_data.english
                    + updated_data.science
                )
                / 3,
                2,
            )
            updated_student = {
                "id": student_id,
                "name": updated_data.name,
                "math": updated_data.math,
                "english": updated_data.english,
                "science": updated_data.science,
                "average": average,
            }

            students[index] = updated_student

            return updated_student
    raise HTTPException(
        status_code=404,
        detail="Student not found",
    )


@router.delete(
    "/{student_id}",
    response_model=DeleteStudentResponse,
)
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
