from typing import Literal

from sqlalchemy import func
from sqlmodel import Session, select

from app.data import students
from app.db_models import Student
from app.models import StudentCreate, StudentUpdate


def calculate_average(
        math: float,
        english: float,
        science: float,
) -> float:
    average_score = (math + english + science) / 3
    return round(average_score, 2)


def list_students(
        session: Session,
        passed: bool | None = None,
        minimum_average: float | None = None,
        sort_order: Literal["asc", "desc"] | None = None,
        offset: int = 0,
        limit: int = 10,
) -> dict:
    statement = select(Student)

    conditions = []
    if passed is not None:
        if passed:
            conditions.append(Student.average >= 5)
        else:
            conditions.append(Student.average < 5)

    if minimum_average is not None:
        conditions.append(Student.average >= minimum_average)

    if conditions:
        statement = statement.where(
            *conditions
        )

    if sort_order == "asc":
        statement = statement.order_by(
            Student.average.asc()
        )
    elif sort_order == "desc":
        statement = statement.order_by(
            Student.average.desc()
        )

    count_statement = (
        select(func.count())
        .select_from(Student)
    )

    if conditions:
        count_statement = count_statement.where(
            *conditions
        )
    total = session.exec(
        count_statement
    ).one()

    statement = (
        statement.offset(offset)
        .limit(limit)
    )
    db_students = session.exec(
        statement
    ).all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(db_students),
        "students": db_students,
    }


def get_student_by_id(session: Session, student_id: int) -> Student | None:
    return session.get(Student, student_id)


def create_student(
        session: Session,
        student_data: StudentCreate
) -> Student:
    average = calculate_average(
        student_data.math,
        student_data.english,
        student_data.science
    )
    db_student = Student(
        name=student_data.name,
        math=student_data.math,
        english=student_data.english,
        science=student_data.science,
        average=average
    )
    session.add(db_student)
    session.commit()
    session.refresh(db_student)

    return db_student


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
    for index, student in enumerate(students):
        if student["id"] == student_id:
            deleted_student = students.pop(index)
            return deleted_student
    return None
