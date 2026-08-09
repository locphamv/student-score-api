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


def test_update_student(client: TestClient):
    create_response = client.post(
        "/students",
        json={
            "name": "An",
            "math": 8,
            "english": 7,
            "science": 9,
        }
    )

    student_id = create_response.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "An Nguyen",
            "math": 9,
            "english": 8,
            "science": 10,
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == student_id
    assert data["name"] == "An Nguyen"
    assert data["math"] == 9
    assert data["english"] == 8
    assert data["science"] == 10
    assert data["average"] == 9


def test_update_student_not_found(
        client: TestClient,
):
    response = client.put(
        "/students/999",
        json={
            "name": "Unknown",
            "math": 8,
            "english": 8,
            "science": 8,
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Student not found",
    }


def test_patch_student(client: TestClient):
    create_response = client.post(
        "/students",
        json={
            "name": "An",
            "math": 8,
            "english": 7,
            "science": 9,
        }
    )

    student_id = create_response.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={
            "math": 10,
        },
    )

    data = response.json()

    assert response.status_code == 200

    assert data["name"] == "An"

    assert data["math"] == 10
    assert data["english"] == 7
    assert data["science"] == 9

    assert data["average"] == 8.67


def test_patch_multiple_fields(
        client: TestClient,
):
    create_response = client.post(
        "/students",
        json={
            "name": "An",
            "math": 8,
            "english": 7,
            "science": 9,
        }
    )

    student_id = create_response.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={
            "name": "An Nguyen",
            "science": 10,
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "An Nguyen"

    assert data["math"] == 8
    assert data["english"] == 7
    assert data["science"] == 10

    assert data["average"] == 8.33


def test_patch_invalid_score(
    client: TestClient,
):
    create_response = client.post(
        "/students",
        json={
            "name": "An",
            "math": 8,
            "english": 7,
            "science": 9,
        },
    )

    student_id = create_response.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={
            "math": 15,
        }
    )

    assert response.status_code == 422

    def test_delete_student(client: TestClient):
        create_response = client.post(
            "/students",
            json={
                "name": "An",
                "math": 8,
                "english": 7,
                "science": 9,
            },
        )

        student_id = create_response.json()["id"]

        response = client.delete(
            f"/students/{student_id}"
        )

        data = response.json()

        assert response.status_code == 200
        assert data["student"]["id"] == student_id

        get_response = client.get(
            f"/students/{student_id}"
        )

        assert get_response.status_code == 404


def test_delete_student_not_found(
        client: TestClient,
):
    response = client.delete(
        "/students/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Student not found",
    }


def test_sort_students_descending(
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
            name="Binh",
            math=6,
            english=5.5,
            science=7,
            average=6.17,
        ),
        Student(
            name="Chi",
            math=9.5,
            english=9,
            science=8.5,
            average=9,
        ),
    ]

    session.add_all(students)
    session.commit()

    response = client.get(
        "/students?sort_order=desc"
    )

    data = response.json()

    assert response.status_code == 200

    names = [
        student["name"]
        for student in data["students"]
    ]

    assert names == [
        "Chi",
        "An",
        "Binh",
    ]

def test_sort_students_ascending(
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
            name="Binh",
            math=6,
            english=5.5,
            science=7,
            average=6.17,
        ),
        Student(
            name="Chi",
            math=9.5,
            english=9,
            science=8.5,
            average=9,
        ),
    ]

    session.add_all(students)
    session.commit()

    response = client.get(
        "/students?sort_order=asc"
    )

    data = response.json()

    averages = [
        student["average"]
        for student in data["students"]
    ]

    assert averages == [
        6.17,
        8,
        9,
    ]


def test_student_pagination(
    session: Session,
    client: TestClient,
):
    students = [
        Student(
            name="Student 1",
            math=5,
            english=5,
            science=5,
            average=5,
        ),
        Student(
            name="Student 2",
            math=6,
            english=6,
            science=6,
            average=6,
        ),
        Student(
            name="Student 3",
            math=7,
            english=7,
            science=7,
            average=7,
        ),
        Student(
            name="Student 4",
            math=8,
            english=8,
            science=8,
            average=8,
        ),
        Student(
            name="Student 5",
            math=9,
            english=9,
            science=9,
            average=9,
        ),
    ]

    session.add_all(students)
    session.commit()

    response = client.get(
        "/students?"
        "sort_order=asc&"
        "offset=2&"
        "limit=2"
    )

    data = response.json()

    assert response.status_code == 200

    assert data["total"] == 5
    assert data["offset"] == 2
    assert data["limit"] == 2
    assert data["count"] == 2

    assert len(data["students"]) == 2

    assert data["students"][0]["name"] == (
        "Student 3"
    )

    assert data["students"][1]["name"] == (
        "Student 4"
    )

def test_last_page(
    session: Session,
    client: TestClient,
):
    for number in range(1, 6):
        student = Student(
            name=f"Student {number}",
            math=number + 4,
            english=number + 4,
            science=number + 4,
            average=number + 4,
        )

        session.add(student)

    session.commit()

    response = client.get(
        "/students?"
        "sort_order=asc&"
        "offset=4&"
        "limit=2"
    )

    data = response.json()

    assert data["total"] == 5
    assert data["count"] == 1

    assert len(data["students"]) == 1

    assert data["students"][0]["name"] == (
        "Student 5"
    )


def test_filter_sort_and_paginate(
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
            name="Binh",
            math=6,
            english=5.5,
            science=7,
            average=6.17,
        ),
        Student(
            name="Chi",
            math=9.5,
            english=9,
            science=8.5,
            average=9,
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
        "/students?"
        "passed=true&"
        "minimum_average=7&"
        "sort_order=desc&"
        "offset=0&"
        "limit=1"
    )

    data = response.json()

    assert response.status_code == 200

    assert data["total"] == 2
    assert data["count"] == 1

    assert data["students"][0]["name"] == "Chi"


def test_invalid_limit(client: TestClient):
    response = client.get(
        "/students?limit=0"
    )

    assert response.status_code == 422

def test_invalid_offset(client: TestClient):
    response = client.get(
        "/students?offset=-1"
    )

    assert response.status_code == 422

def test_invalid_sort_order(
    client: TestClient,
):
    response = client.get(
        "/students?sort_order=random"
    )

    assert response.status_code == 422
