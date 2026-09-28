from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.storage.database import Base, SessionLocal, engine


class AssessmentRecord(Base):
    __tablename__ = "assessment_records"

    id = Column(String, primary_key=True)
    candidate_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    payload = Column(JSONB, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )


def ensure_assessment_table():
    Base.metadata.create_all(
        bind=engine,
        tables=[AssessmentRecord.__table__]
    )


def create_assessment(candidate_id: str, payload: Dict[str, Any]) -> str:
    ensure_assessment_table()

    assessment_id = str(uuid4())

    db = SessionLocal()

    try:
        record = AssessmentRecord(
            id=assessment_id,
            candidate_id=candidate_id,
            status="pending",
            payload=payload
        )

        db.add(record)
        db.commit()

        return assessment_id

    finally:
        db.close()


def get_assessment(assessment_id: str) -> Optional[AssessmentRecord]:
    ensure_assessment_table()

    db = SessionLocal()

    try:
        return db.query(AssessmentRecord).filter(
            AssessmentRecord.id == assessment_id
        ).first()
    finally:
        db.close()


def update_assessment(
    assessment_id: str,
    payload: Dict[str, Any],
    status: str
):
    ensure_assessment_table()

    db = SessionLocal()

    try:
        record = db.query(AssessmentRecord).filter(
            AssessmentRecord.id == assessment_id
        ).first()

        if not record:
            return None

        record.payload = payload
        record.status = status
        record.updated_at = datetime.now(timezone.utc)

        db.commit()

        return record

    finally:
        db.close()