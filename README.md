Resume Optimiser is a full-stack web application designed to analyze resumes against target job descriptions and optimize them for Applicant Tracking Systems (ATS). Built with a React, TypeScript, and Tailwind CSS frontend paired with a Python FastAPI backend and SQLite database, the system parses .pdf and .docx files to calculate alignment scores, run keyword gap analyses, and generate tailored, impact-driven bullet point recommendations.

Quick Start

Backend:
Bash
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload

Frontend:
Bash
cd frontend && npm install && npm run dev
