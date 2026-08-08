from typing import Literal

from sqlalchemy import func
from sqlmodel import Session, col, select

from app.db_models import Student
from app.models import (
    StudentCreate,
    StudentPatch,
    StudentUpdate,
)


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
        conditions.append(
            Student.average >= minimum_average
        )

    if conditions:
        statement = statement.where(*conditions)

    if sort_order == "asc":
        statement = statement.order_by(
            col(Student.average).asc()
        )
    elif sort_order == "desc":
        statement = statement.order_by(
            col(Student.average).desc()
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
        statement
        .offset(offset)
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


def get_student_by_id(
    session: Session,
    student_id: int,
) -> Student | None:
    return session.get(Student, student_id)


def create_student(
    session: Session,
    student_data: StudentCreate,
) -> Student:
    average = calculate_average(
        student_data.math,
        student_data.english,
        student_data.science,
    )

    db_student = Student(
        name=student_data.name,
        math=student_data.math,
        english=student_data.english,
        science=student_data.science,
        average=average,
    )

    session.add(db_student)
    session.commit()
    session.refresh(db_student)

    return db_student


def update_student(
    session: Session,
    student_id: int,
    updated_data: StudentUpdate,
) -> Student | None:
    db_student = session.get(Student, student_id)

    if db_student is None:
        return None

    average = calculate_average(
        updated_data.math,
        updated_data.english,
        updated_data.science,
    )

    db_student.name = updated_data.name
    db_student.math = updated_data.math
    db_student.english = updated_data.english
    db_student.science = updated_data.science
    db_student.average = average

    session.add(db_student)
    session.commit()
    session.refresh(db_student)

    return db_student


def delete_student(
    session: Session,
    student_id: int,
) -> Student | None:
    db_student = session.get(Student, student_id)

    if db_student is None:
        return None

    session.delete(db_student)
    session.commit()

    return db_student


def patch_student(
        session: Session,
        student_id: int,
        patch_data: StudentPatch,
) -> Student | None:
    # Find the student by primary key
    db_student = session.get(
        Student,
        student_id,
    )

    if db_student is None:
        return None

    # Get only fields sent by the client
    update_data = patch_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    #update only the provided fields
    for field, value in update_data.items():
        setattr(
            db_student,
            field,
            value,
        )

    # Recalculate the average after score changes
    db_student.average = calculate_average(
        db_student.math,
        db_student.english,
        db_student.science,
    )

    session.add(db_student)
    session.commit()
    session.refresh(db_student)

    return db_student
