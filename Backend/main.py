from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from services.parser_service import extract_text_from_pdf, extract_text_from_docx, scrape_job_description
from services.ai_service import analyze_and_optimize_resume

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Optimizer API")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(None),
    job_url: str = Form(None),
    db: Session = Depends(get_db)
):
    # 1. Parse File
    file_bytes = await file.read()
    if file.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(file_bytes)
    elif file.filename.endswith('.docx'):
        resume_text = extract_text_from_docx(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX are supported")

    # 2. Handle Job Description Input
    target_job_text = ""
    if job_url:
        try:
            target_job_text = scrape_job_description(job_url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif job_description:
        target_job_text = job_description
    else:
        raise HTTPException(status_code=400, detail="Provide either a job description or a URL")

    # 3. AI Optimization
    try:
        ai_results = analyze_and_optimize_resume(resume_text, target_job_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 4. Save to DB (Assuming user_id=1 for local standalone MVP)
    new_analysis = models.ResumeAnalysis(
        user_id=1,
        original_text=resume_text,
        job_description=target_job_text,
        ats_score=ai_results.get("ats_score"),
        optimized_text=ai_results.get("optimized_resume_text"),
        gap_analysis=ai_results.get("gap_analysis")
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return {
        "status": "success",
        "data": ai_results,
        "id": new_analysis.id
    }