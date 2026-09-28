# Multi-Agent Candidate Assessment System

An AI-powered multi-agent system for evaluating candidates using resume information, projects, technical assessments, interview evidence, and authorized repository data.

## Overview

The system uses multiple specialized AI agents coordinated by a central Orchestrator Agent.

The agents analyze different parts of candidate information and produce structured findings. Evidence is collected and linked to assessments so that the final report can distinguish between available evidence and AI interpretation.

## Main Workflow

Candidate Input
        ↓
Input Validation
        ↓
Orchestrator Agent
        ↓
┌───────────────┬───────────────┬───────────────┬───────────────┐
│ Resume Agent  │ Technical     │ Project Agent  │ Repository    │
│               │ Agent         │               │ Agent         │
└───────────────┴───────────────┴───────────────┴───────────────┘
        ↓
Consistency Agent
        ↓
Evidence Agent
        ↓
Evaluation Agent
        ↓
Report Agent
        ↓
Final Candidate Assessment

## Agents

### 1. Orchestrator Agent
Controls the complete workflow and manages dependencies between agents.

### 2. Resume Agent
Extracts skills, education, experience, projects and candidate claims from the resume.

### 3. Technical Agent
Evaluates technical competencies using technical assessment and interview evidence.

### 4. Project Agent
Analyzes project scope, technologies, technical depth and candidate contribution.

### 5. Repository Agent
Analyzes authorized GitHub/GitLab repository information when available.

### 6. Consistency Agent
Compares information from different sources and identifies supported, partial, conflicting or unverified claims.

### 7. Evidence Agent
Maintains a centralized evidence ledger connecting findings to their sources.

### 8. Evaluation Agent
Maps competencies to evidence and produces competency-level assessments with confidence and limitations.

### 9. Report Agent
Generates the final structured candidate assessment report.

## Technology Stack

- Python
- FastAPI
- Google Gemini
- Pydantic
- SQLAlchemy
- PostgreSQL
- PostgreSQL JSONB
- Uvicorn
- Git/GitHub

## Project Structure

```text
Multi-Agent-Candidate-Assessment/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── schemas/
│   ├── services/
│   ├── retrieval/
│   ├── storage/
│   ├── config.py
│   └── main.py
│
├── prompts/
├── tests/
├── data/
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

API Endpoints
POST /api/v1/assessments
GET  /api/v1/assessments/{id}
POST /api/v1/assessments/{id}/run
GET  /api/v1/assessments/{id}/agents
GET  /api/v1/assessments/{id}/evidence
GET  /api/v1/assessments/{id}/conflicts
GET  /api/v1/assessments/{id}/report

Structured Output

Agent responses are validated using Pydantic models. Invalid Gemini JSON responses are retried and validated before being accepted by the system.