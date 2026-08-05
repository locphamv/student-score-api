
from fastapi import FastAPI, HTTPException, Query, status
from app.routers.students import router as students_router


# Create the FastAPI application
app = FastAPI(
    title="Student Score API",
    version="1.0.0",
)

app.include_router(students_router)


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

