from app.storage.database import Base, engine
from app.storage import models
from app.storage.assessment_store import AssessmentRecord


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()