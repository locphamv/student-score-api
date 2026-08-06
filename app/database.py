from pathlib import Path
from sqlmodel import Session,SQLModel, create_engine
from app.db_models import Student

# Build the database path from the project root
project_directory = Path(__file__).resolve().parent.parent
database_path = project_directory/ "student_scores.db"

database_url = f"sqlite:///{database_path}"

# Allow SQLite connections to be used by FastAPI
connect_args = {
    "check_same_thread": False,
}

#Create the database engine
engine = create_engine(
    database_url,
    connect_args = connect_args,
    echo=True,
)

def create_db_and_tables() ->None:
    SQLModel.metadata.create_all(engine)

def get_session():
    #Create one database session for each request
    with Session(engine) as session:
        yield session
        
