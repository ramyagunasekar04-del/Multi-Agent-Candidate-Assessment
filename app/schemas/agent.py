from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentStatus(BaseModel):
    agent_name: str
    status: str = "pending"
    error: Optional[str] = None

    findings: Dict[str, Any] = Field(
        default_factory=dict
    )

    evidence_ids: List[str] = Field(
        default_factory=list
    )

    confidence: float = 0.0

    limitations: List[str] = Field(
        default_factory=list
    )