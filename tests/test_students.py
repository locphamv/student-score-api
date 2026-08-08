from fastapi.testclient import TestClient
from sqlmodel import Session

from app.db_models import Student


def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
    }


def test_create_student(client: TestClient):
    response = client.post(
        "/students",
        json={
            "name": "An",
            "math": 8,
            "english": 7,
            "science": 9,
        },
    )

    data = response.json()

    assert response.status_code == 201

    assert data["id"] is not None
    assert data["name"] == "An"
    assert data["math"] == 8
    assert data["english"] == 7
    assert data["science"] == 9
    assert data["average"] == 8


def test_create_student_invalid_score(
    client: TestClient,
):
    response = client.post(
        "/students",
        json={
            "name": "An",
            "math": 15,
            "english": 7,
            "science": 9,
        },
    )

    assert response.status_code == 422


def test_get_student(client: TestClient):
    create_response = client.post(
        "/students",
        json={
            "name": "Chi",
            "math": 9.5,
            "english": 9,
            "science": 8.5,
        },
    )

    created_student = create_response.json()
    student_id = created_student["id"]

    response = client.get(
        f"/students/{student_id}"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == student_id
    assert data["name"] == "Chi"
    assert data["average"] == 9


def test_get_student_not_found(
    client: TestClient,
):
    response = client.get(
        "/students/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Student not found",
    }


def test_list_students(
    session: Session,
    client: TestClient,
):
    student_1 = Student(
        name="An",
        math=8,
        english=7,
        science=9,
        average=8,
    )

    student_2 = Student(
        name="Dung",
        math=4,
        english=5,
        science=4.5,
        average=4.5,
    )

    session.add(student_1)
    session.add(student_2)
    session.commit()

    response = client.get("/students")

    data = response.json()

    assert response.status_code == 200
    assert data["total"] == 2
    assert data["count"] == 2
    assert len(data["students"]) == 2


def test_filter_passed_students(
    session: Session,
    client: TestClient,
):
    students = [
        Student(
            name="An",
            math=8,
            english=7,
            science=9,
            average=8,
        ),
        Student(
            name="Dung",
            math=4,
            english=5,
            science=4.5,
            average=4.5,
        ),
    ]

    session.add_all(students)
    session.commit()

    response = client.get(
        "/students?passed=true"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["total"] == 1
    assert data["students"][0]["name"] == "An"
