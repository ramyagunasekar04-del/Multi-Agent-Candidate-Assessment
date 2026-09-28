from app.agents.resume_agent import ResumeAgent


def main():
    state = {
        "candidate": {
            "candidate_id": "CAND-001",
            "target_role": "AI Engineer",
            "resume_text": """
            Ramya is a Python developer interested in Artificial Intelligence
            and Machine Learning.

            Skills:
            Python, SQL, Pandas, NumPy, Scikit-learn, FastAPI,
            Generative AI, Git and GitHub.

            Projects:
            1. AI Recruitment Assessment System
               Built a candidate assessment application using Python,
               FastAPI, Gemini and PostgreSQL.

            2. LLM Behavioural Communication Project
               Built an application to analyze interview communication
               and generate structured reports.

            Education:
            Bachelor's degree in Computer Science.

            Certification:
            Python Programming Certification.
            """
        }
    }

    agent = ResumeAgent()

    print("\nRunning Resume Agent...\n")

    result = agent.run(state)

    print("Agent:", result["agent_name"])
    print("Status:", result["status"])
    print("\nResume Agent Output:")
    print(result["findings"])


if __name__ == "__main__":
    main()