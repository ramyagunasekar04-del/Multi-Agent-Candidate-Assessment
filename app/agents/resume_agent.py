from typing import Any, Dict

from app.agents.base_agent import BaseAgent

class ResumeAgent(BaseAgent):

   def __init__(self):
    super().__init__("resume_agent")

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        candidate = state["candidate"]

        resume_text = candidate["resume_text"]

        prompt = f"""
You are the Resume Agent in a multi-agent candidate assessment system.

Your job is to analyze ONLY the candidate's provided resume.

Candidate ID:
{candidate["candidate_id"]}

Target Role:
{candidate["target_role"]}

Resume:
{resume_text}

Extract the following:

1. Skills
2. Work experience
3. Education
4. Certifications
5. Projects
6. Explicit candidate claims
7. Evidence snippets from the resume
8. Confidence
9. Limitations

IMPORTANT RULES:

- Use only information explicitly present in the resume.
- Do not invent skills, experience, qualifications, projects or certifications.
- Do not assume expertise from a job title alone.
- Separate candidate claims from demonstrated evidence.
- If information is missing, report it as missing.
- Return structured JSON.
"""

        result = self.ask_gemini(prompt)

        return {
    "agent_name": self.name,
    "status": "completed",
    "findings": result["findings"],
    "evidence_ids": result["evidence_ids"],
    "confidence": result["confidence"],
    "limitations": result["limitations"]
}