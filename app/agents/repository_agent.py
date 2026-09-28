from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class RepositoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("repository_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        candidate = state["candidate"]

        repositories = candidate.get("repository_data", [])

        if not repositories:
            return {
                "agent_name": self.name,
                "status": "completed",
                "findings": {
                    "status": "unavailable",
                    "message": "Repository evidence was not provided."
                },
                "evidence_ids": [],
                "confidence": 0.0,
                "limitations": [
                    "No authorized repository data available."
                ]
            }

        prompt = f"""
You are the Repository Agent.

Analyze only the authorized repository information below.

Repository data:
{repositories}

Identify:

- repository/project structure
- programming languages
- relevant technologies
- documentation evidence
- testing evidence
- configuration evidence
- implementation evidence
- relationship to claimed skills
- limitations

Do not treat commit count alone as proof of technical skill.

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