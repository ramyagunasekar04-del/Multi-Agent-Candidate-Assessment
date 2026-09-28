import asyncio
from datetime import datetime
from typing import Any, Dict

from app.agents.resume_agent import ResumeAgent
from app.agents.technical_agent import TechnicalAgent
from app.agents.project_agent import ProjectAgent
from app.agents.repository_agent import RepositoryAgent
from app.agents.consistency_agent import ConsistencyAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.agents.report_agent import ReportAgent


class Orchestrator:

    def __init__(self):
        self.independent_agents = [
            ResumeAgent(),
            TechnicalAgent(),
            ProjectAgent(),
            RepositoryAgent()
        ]

        self.consistency_agent = ConsistencyAgent()
        self.evidence_agent = EvidenceAgent()
        self.evaluation_agent = EvaluationAgent()
        self.report_agent = ReportAgent()

    async def run_agent(
        self,
        agent,
        state: Dict[str, Any]
    ):
        try:
            state["workflow_status"][agent.name] = {
                "status": "running",
                "started_at": datetime.utcnow().isoformat()
            }

            result = await asyncio.to_thread(
                agent.run,
                state
            )

            state["agent_outputs"][agent.name] = result

            state["workflow_status"][agent.name] = {
                "status": "completed",
                "completed_at": datetime.utcnow().isoformat()
            }

            return result

        except Exception as exc:

            state["agent_outputs"][agent.name] = {
                "agent_name": agent.name,
                "status": "failed",
                "findings": {},
                "error": str(exc),
                "evidence_ids": [],
                "confidence": 0.0,
                "limitations": [
                    "Agent execution failed."
                ]
            }

            state["workflow_status"][agent.name] = {
                "status": "failed",
                "completed_at": datetime.utcnow().isoformat()
            }

            return state["agent_outputs"][agent.name]

    async def run(self, state: Dict[str, Any]):

        state["workflow_status"]["orchestrator"] = {
            "status": "running",
            "started_at": datetime.utcnow().isoformat()
        }

        # Independent agents run in parallel
        await asyncio.gather(
            *[
                self.run_agent(agent, state)
                for agent in self.independent_agents
            ]
        )

        # Dependent agents
        consistency = await self.run_agent(
            self.consistency_agent,
            state
        )

        state["conflicts"].append(consistency.get("findings", {}))

        evidence = await self.run_agent(
            self.evidence_agent,
            state
        )

        state["evidence"].append(evidence.get("findings", {}))

        evaluation = await self.run_agent(
            self.evaluation_agent,
            state
        )

        state["competencies"].append(
            evaluation.get("findings", {})
        )

        report = await self.run_agent(
            self.report_agent,
            state
        )

        state["final_assessment"] = report.get(
            "findings",
            {}
        )

        state["workflow_status"]["orchestrator"] = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat()
        }

        return state