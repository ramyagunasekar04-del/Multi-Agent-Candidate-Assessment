from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)

from app.storage.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(String(100), unique=True, nullable=False)
    target_role = Column(String(200), nullable=False)
    resume_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=True
    )
    target_role = Column(String(200))
    job_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(String(100), unique=True, nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    status = Column(String(50), default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    agent_name = Column(String(100), nullable=False)
    status = Column(String(50), default="pending")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)


class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    agent_name = Column(String(100), nullable=False)
    output = Column(JSON)
    confidence = Column(Float, default=0.0)
    limitations = Column(JSON)


class EvidenceRecord(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True)
    evidence_id = Column(String(100), unique=True, nullable=False)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    source_type = Column(String(100))
    source_reference = Column(String(255))
    claim = Column(Text)
    supports = Column(JSON)
    evidence_text = Column(Text)
    confidence = Column(Float, default=0.0)


class CompetencyRecord(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    competency = Column(String(200))
    level = Column(String(100))
    evidence_ids = Column(JSON)
    confidence = Column(Float, default=0.0)
    limitations = Column(JSON)


class ConflictRecord(Base):
    __tablename__ = "conflicts"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    claim = Column(Text)
    available_evidence = Column(JSON)
    result = Column(String(100))
    confidence = Column(Float, default=0.0)


class FinalAssessment(Base):
    __tablename__ = "final_assessments"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    assessment = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(
        Integer,
        ForeignKey("assessment_sessions.id")
    )
    report = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)