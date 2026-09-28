from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class EvaluationAgent(BaseAgent):

    def __init__(self):
        super().__init__("evaluation_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        prompt = f"""
You are the Evaluation Agent.

Create a competency-level assessment.

Candidate:
{state.get("candidate")}

Agent findings:
{state.get("agent_outputs")}

Conflicts:
{state.get("conflicts")}

Evidence:
{state.get("evidence")}

For every competency return:

competency
level
evidence_ids
confidence
limitations

Possible competency levels:

Beginner
Intermediate
Advanced
Insufficient Evidence

Do not evaluate using unsupported claims.
Every important assessment should reference evidence.
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