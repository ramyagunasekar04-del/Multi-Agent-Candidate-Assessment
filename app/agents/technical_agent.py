from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class TechnicalAgent(BaseAgent):

    def __init__(self):
        super().__init__("technical_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        candidate = state["candidate"]

        prompt = f"""
You are the Technical Agent.

Evaluate the candidate for the target role using ONLY available evidence.

Target role:
{candidate["target_role"]}

Job description:
{candidate["job_description"]}

Resume:
{candidate["resume_text"]}

Technical assessment:
{candidate.get("technical_assessment", [])}

Interview evidence:
{candidate.get("interview_evidence", [])}

Return JSON containing:

competencies,
findings,
evidence,
confidence,
limitations.

Rules:
- Separate claimed skills from demonstrated skills.
- Never invent evidence.
- Missing evidence must be reported.
- Consider technical assessments and interviews when available.
"""

        result = self.ask_gemini(prompt)

        return {
            "agent_name": self.name,
            "status": "completed",
            "findings": result,
            "evidence_ids": [],
            "confidence": 0.0,
            "limitations": []
        }