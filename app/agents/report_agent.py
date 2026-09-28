from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class ReportAgent(BaseAgent):

    def __init__(self):
        super().__init__("report_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        prompt = f"""
You are the Report Agent.

Generate the final candidate assessment using the supplied information.

Candidate:
{state.get("candidate")}

Evidence:
{state.get("evidence")}

Conflicts:
{state.get("conflicts")}

Competencies:
{state.get("competencies")}

Agent outputs:
{state.get("agent_outputs")}

Create two sections:

1. Candidate-facing assessment
   - strengths
   - gaps
   - evidence
   - improvement areas

2. Reviewer/recruiter-facing assessment
   - competency assessment
   - evidence
   - consistency findings
   - confidence
   - limitations

Clearly separate evidence from AI interpretation.

Do not expose hidden reasoning or chain-of-thought.

Return structured JSON.
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