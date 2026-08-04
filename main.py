from fastapi import FastAPI, HTTPException


# Create the FastAPI application
app = FastAPI()

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
