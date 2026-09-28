from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CandidateInput(BaseModel):
    candidate_id: str
    target_role: str
    job_description: str
    resume_text: str
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    repository_data: List[Dict[str, Any]] = Field(default_factory=list)
    technical_assessment: List[Dict[str, Any]] = Field(default_factory=list)
    interview_evidence: List[Dict[str, Any]] = Field(default_factory=list)


class Evidence(BaseModel):
    evidence_id: str
    source_type: str
    source_reference: str
    claim: str
    supports: List[str] = Field(default_factory=list)
    evidence_text: str
    confidence: float = 0.0


class AgentOutput(BaseModel):
    agent_name: str
    status: str
    findings: Dict[str, Any] = Field(default_factory=dict)
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    limitations: List[str] = Field(default_factory=list)


class Conflict(BaseModel):
    claim: str
    available_evidence: List[str] = Field(default_factory=list)
    result: str
    confidence: float = 0.0


class Competency(BaseModel):
    competency: str
    level: str
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    limitations: List[str] = Field(default_factory=list)


class WorkflowStatus(BaseModel):
    status: str = "pending"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class CandidateState(BaseModel):
    candidate: CandidateInput
    job: Dict[str, Any] = Field(default_factory=dict)

    evidence: List[Evidence] = Field(default_factory=list)

    agent_outputs: Dict[str, AgentOutput] = Field(default_factory=dict)

    conflicts: List[Conflict] = Field(default_factory=list)

    competencies: List[Competency] = Field(default_factory=list)

    workflow_status: Dict[str, WorkflowStatus] = Field(
        default_factory=dict
    )

    final_assessment: Optional[Dict[str, Any]] = None