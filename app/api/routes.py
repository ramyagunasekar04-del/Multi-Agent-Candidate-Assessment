import inspect
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.schemas.candidate import CandidateInput
from app.agents.orchestrator import Orchestrator

from app.storage.assessment_store import (
    create_assessment,
    get_assessment,
    update_assessment,
    ensure_assessment_table,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Assessments"]
)


# Make sure PostgreSQL persistence table exists
ensure_assessment_table()


def record_to_response(record):
    if not record:
        return None

    payload = record.payload or {}

    return {
        "assessment_id": record.id,
        "candidate_id": record.candidate_id,
        "status": record.status,
        "data": payload,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }


@router.post("/assessments")
def create_new_assessment(candidate: CandidateInput):

    payload = {
        "candidate": jsonable_encoder(candidate.model_dump()),
        "job": {
            "target_role": candidate.target_role,
            "job_description": candidate.job_description,
        },
        "evidence": [],
        "agent_outputs": {},
        "conflicts": [],
        "competencies": [],
        "workflow_status": {},
        "final_assessment": None,
    }

    assessment_id = create_assessment(
        candidate_id=candidate.candidate_id,
        payload=payload,
    )

    return {
        "message": "Assessment created successfully",
        "assessment_id": assessment_id,
        "candidate_id": candidate.candidate_id,
        "status": "pending",
    }


@router.get("/assessments/{assessment_id}")
def get_assessment_details(assessment_id: str):

    record = get_assessment(assessment_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    return record_to_response(record)


@router.post("/assessments/{assessment_id}/run")
async def run_assessment(assessment_id: str):

    record = get_assessment(assessment_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    payload = record.payload or {}

    # Prevent accidental duplicate running
    if record.status == "running":
        return {
            "assessment_id": assessment_id,
            "status": "running",
            "message": "Assessment is already running"
        }

    update_assessment(
        assessment_id,
        payload,
        "running"
    )

    try:

        state = {
            "candidate": payload.get("candidate", {}),
            "job": payload.get("job", {}),
            "evidence": payload.get("evidence", []),
            "agent_outputs": payload.get("agent_outputs", {}),
            "conflicts": payload.get("conflicts", []),
            "competencies": payload.get("competencies", []),
            "workflow_status": payload.get("workflow_status", {}),
            "final_assessment": payload.get("final_assessment"),
        }

        orchestrator = Orchestrator()

        result = orchestrator.run(state)

        # Support both async and normal orchestrators
        if inspect.isawaitable(result):
            result = await result

        if result is None:
            result = state

        result = jsonable_encoder(result)

        update_assessment(
            assessment_id,
            result,
            "completed"
        )

        return {
            "assessment_id": assessment_id,
            "status": "completed",
            "message": "Assessment completed successfully",
            "result": result,
        }

    except Exception as exc:

        payload["error"] = str(exc)

        update_assessment(
            assessment_id,
            payload,
            "failed"
        )

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Assessment execution failed",
                "error": str(exc),
            }
        )


@router.get("/assessments/{assessment_id}/agents")
def get_agent_outputs(assessment_id: str):

    record = get_assessment(assessment_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    payload = record.payload or {}

    return {
        "assessment_id": assessment_id,
        "status": record.status,
        "agents": payload.get("agent_outputs", {}),
        "workflow_status": payload.get("workflow_status", {}),
    }


@router.get("/assessments/{assessment_id}/evidence")
def get_evidence(assessment_id: str):

    record = get_assessment(assessment_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    payload = record.payload or {}

    return {
        "assessment_id": assessment_id,
        "evidence": payload.get("evidence", []),
    }


@router.get("/assessments/{assessment_id}/conflicts")
def get_conflicts(assessment_id: str):

    record = get_assessment(assessment_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    payload = record.payload or {}

    return {
        "assessment_id": assessment_id,
        "conflicts": payload.get("conflicts", []),
    }


@router.get("/assessments/{assessment_id}/report")
def get_report(assessment_id: str):

    record = get_assessment(assessment_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    payload = record.payload or {}

    return {
        "assessment_id": assessment_id,
        "status": record.status,
        "final_assessment": payload.get("final_assessment"),
        "report": payload.get("report"),
    }