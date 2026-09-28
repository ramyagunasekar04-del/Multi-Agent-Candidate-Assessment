import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, Field, ValidationError
from google import genai

from app.config import settings


class LLMResponse(BaseModel):
    findings: Dict[str, Any] = Field(default_factory=dict)
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    limitations: list[str] = Field(default_factory=list)


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def ask_gemini(self, prompt: str) -> Dict[str, Any]:
        """
        Generate and validate structured JSON from Gemini.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text.strip()

        # Remove accidental markdown JSON fences
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

        try:
            parsed = json.loads(raw_text)

            validated = LLMResponse.model_validate(parsed)

            return validated.model_dump()

        except (json.JSONDecodeError, ValidationError) as first_error:

            # One safe recovery attempt
            retry_prompt = f"""
Your previous response was not valid according to the required JSON schema.

Return ONLY valid JSON.

Required structure:

{{
  "findings": {{}},
  "evidence_ids": [],
  "confidence": 0.0,
  "limitations": []
}}

Rules:
- findings must be a JSON object
- evidence_ids must be a JSON array of strings
- confidence must be a number between 0 and 1
- limitations must be a JSON array of strings
- do not use markdown
- do not add explanations outside JSON

Previous response:
{raw_text}

Original task:
{prompt}
"""

            retry_response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=retry_prompt
            )

            retry_text = retry_response.text.strip()

            if retry_text.startswith("```"):
                retry_text = retry_text.replace("```json", "")
                retry_text = retry_text.replace("```", "")
                retry_text = retry_text.strip()

            try:
                retry_parsed = json.loads(retry_text)

                validated = LLMResponse.model_validate(
                    retry_parsed
                )

                return validated.model_dump()

            except (json.JSONDecodeError, ValidationError) as second_error:

                raise ValueError(
                    "Gemini returned invalid structured output "
                    "after retry. "
                    f"Initial error: {first_error}. "
                    f"Retry error: {second_error}"
                )

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass