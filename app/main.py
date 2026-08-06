from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers.students import router as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables before receiving requests
    create_db_and_tables()

    yield

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
