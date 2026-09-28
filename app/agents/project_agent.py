from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class ProjectAgent(BaseAgent):

    def __init__(self):
        super().__init__("project_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        candidate = state["candidate"]

        prompt = f"""
You are the Project Agent.

Analyze the candidate's project evidence.

Target role:
{candidate["target_role"]}

Projects:
{candidate.get("projects", [])}

Resume:
{candidate["resume_text"]}

For every available project identify:

- project objective
- technologies
- architecture if supported
- apparent technical depth
- candidate-stated contribution
- verified evidence
- missing information
- limitations

Return structured JSON.

Rules:
- Do not invent architecture or technologies.
- Clearly separate stated contribution from verified evidence.
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