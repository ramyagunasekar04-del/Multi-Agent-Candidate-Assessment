from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class ConsistencyAgent(BaseAgent):

    def __init__(self):
        super().__init__("consistency_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        outputs = state.get("agent_outputs", {})

        prompt = f"""
You are the Consistency Agent.

Compare candidate claims against available evidence from different agents.

Agent outputs:
{outputs}

For each important claim classify it as:

Supported
Partially Supported
Conflicting
Unverified

Return JSON containing:

claims,
conflicts,
confidence,
limitations.

Important:
- Detect disagreement rather than silently selecting one source.
- Do not fabricate compromise values.
- If evidence is insufficient, use "Insufficient evidence".
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