from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database import get_session
from app.models import (
    DeleteStudentResponse,
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)
from app.services import student_service


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
    session: Session = Depends(get_session),
):
    return student_service.list_students(
        session=session,
        passed=passed,
        minimum_average=minimum_average,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student(
    student_id: int,
    session: Session = Depends(get_session),
):
    student = student_service.get_student_by_id(
        session,
        student_id,
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentCreate,
    session: Session = Depends(get_session),
):
    return student_service.create_student(
        session,
        student,
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_id: int,
    updated_data: StudentUpdate,
    session: Session = Depends(get_session),
):
    updated_student = student_service.update_student(
        session,
        student_id,
        updated_data,
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return updated_student


@router.delete(
    "/{student_id}",
    response_model=DeleteStudentResponse,
)
def delete_student(
    student_id: int,
    session: Session = Depends(get_session),
):
    deleted_student = student_service.delete_student(
        session,
        student_id,
    )

    if deleted_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return {
        "message": "Student deleted successfully",
        "student": deleted_student,
    }
