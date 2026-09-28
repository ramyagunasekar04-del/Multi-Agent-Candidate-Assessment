from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class EvidenceAgent(BaseAgent):

    def __init__(self):
        super().__init__("evidence_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        outputs = state.get("agent_outputs", {})

        prompt = f"""
You are the Evidence Agent.

Create a centralized evidence ledger from the available agent findings.

Agent findings:
{outputs}

For every important piece of evidence create:

evidence_id
source_type
source_reference
claim
supports
evidence_text
confidence

Rules:
- Evidence must come from supplied information.
- Never invent evidence.
- Preserve missing or conflicting evidence.
- Link findings to evidence IDs.
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