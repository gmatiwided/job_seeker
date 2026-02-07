"""
CV Generator Tool
Generates ATS-optimized plain text CVs using Google GenAI
"""

import json
import os
import re
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from langchain_core.tools import tool, BaseTool
from google import genai
from google.genai import types
from typing import Type


class CVGeneratorInput(BaseModel):
    """Input schema for CV generation tool"""
    job_offer: str = Field(description="The job offer description including requirements and responsibilities")
    user_profile: str = Field(description="User profile with personal information, skills, experience, etc.")
    job_assessment: str = Field(description="Job assessment with the job offer and user profile")


def generate_cv_sync(job_offer: str, user_profile: str, job_assessment: str) -> str:
    """
    Generates an ATS-friendly CV in PLAIN TEXT format based on the job offer and user profile.
    Synchronous version - no async/await needed.
    
    Args:
        job_offer: The job offer description
        user_profile: User profile as string (YAML format)
        job_assessment: Assessment of job match
        
    Returns:
        ATS-friendly CV in plain text format
    """
    prompt = """You are a professional CV writer and ATS optimization expert.

Your task is to generate an ATS-friendly CV in PLAIN TEXT (.txt format only) based strictly on:
1) The provided candidate profile details
2) The provided job description

CRITICAL RULES (MUST FOLLOW):
- DO NOT invent, assume, exaggerate, or infer any information.
- DO NOT add skills, tools, experience, metrics, certifications, or achievements that are not explicitly mentioned in the profile details.
- If a required section has no relevant information, omit the section entirely.
- Do NOT use tables, columns, graphics, icons, emojis, or special characters.
- Use simple, ATS-compatible formatting only.
- Use standard job-relevant keywords ONLY if they already appear in the profile or job description.
- Do NOT include personal opinions, summaries, or explanations outside the CV content.

OUTPUT FORMAT:
- Plain text (.txt)
- No markdown
- No bullet symbols other than hyphens (-)
- One page where possible
- Clean spacing and clear section headers

CV STRUCTURE (USE THIS ORDER):

NAME
Job Title (aligned with job description, if supported by profile)
City, Country | Email | Phone | LinkedIn | GitHub (only if provided)

PROFESSIONAL SUMMARY
- 2-3 concise lines
- Written strictly from the provided profile
- Aligned to the job description without adding new facts

SKILLS
- List skills exactly as provided
- Group logically if applicable (e.g., Technical Skills, Tools)

PROFESSIONAL EXPERIENCE
Job Title - Company Name
Location | Start Date - End Date
- Achievement or responsibility (fact-based, no assumptions)
- Use action verbs but no fabricated metrics

(Repeat for all roles provided)

PROJECTS (ONLY IF PROVIDED)
Project Name
- Brief description based strictly on given details
- Technologies used (only if explicitly mentioned)

EDUCATION
Degree - Field of Study
Institution Name | Location | Graduation Year (if provided)

CERTIFICATIONS (ONLY IF PROVIDED)
- Certification Name - Issuing Organization - Year

ADDITIONAL INFORMATION (OPTIONAL)
- Languages
- Publications
- Volunteer experience
(Only include if explicitly provided)

FINAL CHECK BEFORE OUTPUT:
- No hallucinated content
- No formatting that breaks ATS parsing
- CV content reflects only provided data
- Output is plain text only
"""
    
    input_data = f"""INPUT DATA:

Candidate Profile:
{user_profile}

Job Description:
{job_offer}

Job Assessment:
{job_assessment}"""
    
    try:
        # Get unified LLM client
        api_key = "AIzaSyAYY4TTtVcOjisOt6nFcx0xppSyBCUKayo"
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=input_data,
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                max_output_tokens=4000,
                temperature=0.3,
            ),
        )

        return response.text
    except Exception as e:
        return f"Error generating CV: {str(e)}"


@tool("generate_cv", return_direct=False)
def generate_cv_tool(job_offer: str, user_profile: str, job_assessment: str) -> str:
    """
    Generates an ATS-friendly CV in PLAIN TEXT format based on the job offer and user profile.
    Returns CV text ready to be saved as .txt file.
    
    CRITICAL: Only uses information explicitly provided in user_profile.
    Does NOT invent, assume, or exaggerate any information.
    
    Args:
        job_offer: The job offer description
        user_profile: User profile as string (YAML format)
        job_assessment: Assessment of job match
        
    Returns:
        ATS-friendly CV in plain text format
    """
    return generate_cv_sync(job_offer, user_profile, job_assessment)


class CVGeneratorTool(BaseTool):
    """
    LangChain tool for generating ATS-friendly CVs.
    Synchronous implementation - no async needed.
    """
    name: str = "generate_cv"
    description: str = "Generates an ATS-friendly CV in PLAIN TEXT format based on the job offer and user profile. Returns CV text ready to be saved as .txt file."
    args_schema: Type[BaseModel] = CVGeneratorInput
    return_direct: bool = False
    
    def _run(self, job_offer: str, user_profile: str, job_assessment: str) -> str:
        """Synchronous run"""
        return generate_cv_sync(job_offer, user_profile, job_assessment)
    
    def _arun(self, job_offer: str, user_profile: str, job_assessment: str) -> str:
        """Async run - just calls sync version"""
        return self._run(job_offer, user_profile, job_assessment)
