import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini Client
# It automatically looks for the GEMINI_API_KEY environment variable
client = genai.Client()

def analyze_and_optimize_resume(resume_text: str, job_description: str):
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) software and Executive Recruiter.
    I will provide a RESUME and a JOB DESCRIPTION.
    
    Perform the following tasks:
    1. Calculate an ATS compatibility score (0-100).
    2. Identify missing keywords and skills.
    3. Rewrite the resume bullet points to better match the job requirements, utilizing action verbs and quantifying results.
    4. Provide a brief gap analysis.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    """

    try:
        # Call Gemini using the fast and free gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                # System instructions force Gemini to behave like a strict ATS reviewer
                system_instruction="You are a helpful assistant designed to output strict JSON. Do not include markdown wrappers like ```json.",
                # This configuration forces Gemini to return a valid JSON structure matching our schema
                response_mime_type="application/json",
                response_schema=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "ats_score": types.Schema(type=types.Type.INTEGER),
                        "missing_keywords": types.Schema(
                            type=types.Type.ARRAY, 
                            items=types.Schema(type=types.Type.STRING)
                        ),
                        "gap_analysis": types.Schema(type=types.Type.STRING),
                        "optimized_resume_text": types.Schema(type=types.Type.STRING),
                    },
                    required=["ats_score", "missing_keywords", "gap_analysis", "optimized_resume_text"],
                ),
                temperature=0.3
            ),
        )
        
        # Parse and return the JSON response
        return json.loads(response.text)
        
    except Exception as e:
        raise Exception(f"Gemini AI Analysis failed: {str(e)}")