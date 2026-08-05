from typing import Literal

from app.data import students
from app.models import StudentCreate, StudentUpdate


def calculate_average(
        math: float,
        english: float,
        science: float,
) -> float:
    average_score = (math + english + science) / 3
    return round(average_score, 2)


def list_students(
        passed: bool | None = None,
        minimum_average: float | None = None,
        sort_order: Literal["asc", "desc"] | None = None,
        offset: int = 0,
        limit: int = 10,
) -> dict:
    result = students.copy()
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

    if minimum_average is not None:
        result = [
            student
            for student in result
            if student["average"] >= minimum_average
        ]
    if sort_order is not None:
        result.sort(
            key=lambda student: student["average"],
            reverse=sort_order == "desc"
        )
    total = len(result)
    paginated_students = result[offset: offset+limit]

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(paginated_students),
        "students": paginated_students
    }


def get_student_by_id(student_id: int) -> dict | None:
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def create_student(student_data: StudentCreate) -> dict:
    if students:
        new_id = max(
            student["id"]
            for student in students
        ) + 1
    else:
        new_id = 1

    average = calculate_average(
        student_data.math,
        student_data.english,
        student_data.science
    )
    new_student = {
        "id": new_id,
        "name": student_data.name,
        "math": student_data.math,
        "english": student_data.english,
        "science": student_data.science,
        "average": average
    }
    students.append(new_student)
    return new_student


def update_student(
    student_id: int,
    updated_data: StudentUpdate,
) -> dict | None:
    for index, student in enumerate(students):
        if student["id"] == student_id:
            average = calculate_average(
                updated_data.math,
                updated_data.english,
                updated_data.science
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

    return None


def delete_student(student_id: int) -> dict | None:
    for index,student in enumerate(students):
        if student["id"] == student_id:
            deleted_student = students.pop(index)
            return deleted_student
    return None
