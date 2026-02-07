"""
Job Assessment Tool
Assesses candidate's fit for a job offer based on their profile
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from typing import Type
from langchain_core.tools import BaseTool

class JobAssessmentInput(BaseModel):
    """Input schema for job assessment tool"""
    job_offer: str = Field(description="The job offer description")
    user_profile: dict = Field(description="User profile with skills and experience")


class JobAssessmentOutput(BaseModel):
    """Output schema for job assessment tool"""
    assessment: str = Field(description="Executive summary of the job match (2-3 sentences with overall evaluation)")
    match_score: float = Field(description="Match score from 0 to 100 based on weighted criteria")
    strengths: list[str] = Field(description="3-7 specific strengths that align with the role, with concrete examples")
    gaps: list[str] = Field(description="2-5 specific gaps, missing skills, or areas of concern")
    recommendations: list[str] = Field(description="4-6 actionable recommendations for application and skill development")


def assess_job_match(job_offer: str, user_profile: str) -> JobAssessmentOutput:
    """
    Assesses the candidate's fit for a job offer based on their profile.
    Returns a detailed assessment report with match score, strengths, gaps, and recommendations.
    """
    prompt = """You are an expert job match assessor and career consultant with deep expertise in talent evaluation, skills assessment, and career development.

Your task is to provide a comprehensive, honest, and actionable assessment of how well a candidate matches a specific job opportunity.

ASSESSMENT CRITERIA:

1. SKILLS MATCH (40% of total score)
   - Evaluate technical skills alignment with job requirements
   - Consider both hard skills (programming languages, tools, frameworks) and soft skills
   - Match required skills vs. candidate's skills
   - Weight "required" skills more heavily than "nice-to-have" skills

2. EXPERIENCE LEVEL (30% of total score)
   - Compare years of experience required vs. candidate's experience
   - Evaluate relevance of experience (same industry/domain is a plus)
   - Consider quality over quantity - relevant experience counts more
   - Assess if candidate is overqualified, underqualified, or appropriately qualified

3. DOMAIN/INDUSTRY KNOWLEDGE (15% of total score)
   - Assess experience in the same or similar industry
   - Evaluate transferable knowledge from related domains
   - Consider specific domain expertise mentioned in requirements

4. EDUCATION & CERTIFICATIONS (10% of total score)
   - Match educational requirements with candidate's qualifications
   - Consider relevant certifications and continuous learning
   - Assess if education compensates for experience gaps or vice versa

5. CULTURAL & ROLE FIT (5% of total score)
   - Work style alignment (Agile, remote, collaborative, etc.)
   - Career trajectory and growth potential
   - Location and work arrangement compatibility

SCORING GUIDELINES:

- 90-100: Exceptional match - Candidate exceeds most requirements, likely a top performer
- 80-89: Strong match - Candidate meets all core requirements and some preferred qualifications
- 70-79: Good match - Candidate meets most requirements with minor gaps
- 60-69: Moderate match - Candidate has foundational fit but notable gaps exist
- 50-59: Weak match - Significant gaps in required skills or experience
- Below 50: Poor match - Major misalignment with job requirements

CRITICAL RULES:

1. HONESTY & ACCURACY
   - Be truthful about gaps and weaknesses
   - Don't oversell or undersell the candidate
   - Provide realistic assessment based on actual requirements
   - Base all conclusions on provided data only

2. NO ASSUMPTIONS
   - Only use information explicitly stated in the profile
   - Don't assume skills or experience not mentioned
   - Don't infer capabilities without evidence
   - If information is missing, note it as a gap or unknown

3. CONSTRUCTIVE FEEDBACK
   - Frame gaps as opportunities for growth
   - Provide actionable recommendations
   - Be specific about what would improve the match
   - Maintain professional and encouraging tone

4. CONTEXT AWARENESS
   - Consider seniority level appropriately (junior vs senior roles)
   - Account for career transitions and learning curves
   - Recognize transferable skills from adjacent fields
   - Understand that perfect matches are rare

OUTPUT STRUCTURE:

1. ASSESSMENT (string):
   - Executive summary (2-3 sentences)
   - Overall match evaluation
   - Key finding or headline

2. MATCH_SCORE (float 0-100):
   - Calculated based on the criteria above
   - Weighted average considering all factors
   - Be precise and justified

3. STRENGTHS (list of strings):
   - 3-7 specific strengths that align with the role
   - Include concrete examples from profile
   - Focus on job-relevant capabilities
   - Prioritize most impactful strengths

4. GAPS (list of strings):
   - 2-5 specific gaps or areas of concern
   - Be honest but constructive
   - Include both skill gaps and experience gaps
   - Note if gaps are "deal-breakers" or "nice-to-haves"
   - If no significant gaps, mention minor areas for growth

5. RECOMMENDATIONS (list of strings):
   - 4-6 actionable recommendations
   - Mix of application strategy and skill development
   - Specific to this candidate and job
   - Include CV/interview preparation tips
   - Suggest how to address gaps or highlight strengths

EXAMPLES OF GOOD OUTPUTS:

Strengths:
- "2 years of hands-on Python experience with pandas, scikit-learn matches core technical requirements"
- "Master's degree in Data Science from recognized institution fulfills educational requirement"
- "Direct logistics/supply chain analytics experience aligns perfectly with company domain"

Gaps:
- "Missing required 5+ years experience (has 2 years) - may be considered junior for this role"
- "No mention of TensorFlow or PyTorch which are listed as preferred qualifications"
- "Limited cloud platform experience (AWS/GCP/Azure) mentioned in nice-to-have section"

Recommendations:
- "Emphasize the 12% efficiency improvement achievement to demonstrate impact despite shorter tenure"
- "In cover letter, explain how master's degree and intensive projects compensate for experience gap"
- "Prepare examples of complex data pipeline work to address scalability concerns"
- "Consider pursuing AWS or GCP certification to strengthen cloud skills"
- "Highlight collaborative cross-functional work to match team-oriented culture"

REMEMBER:
- Be thorough but concise
- Support claims with evidence from profile
- Balance honesty with encouragement
- Provide value to both candidate and potential employer perspective
- Focus on actionable insights"""

    input_data = f"""INPUT DATA:

Job Offer:
{job_offer}

Candidate Profile:
{user_profile}

Please provide a comprehensive job match assessment following the structure and guidelines above."""
    try:
        # Get unified LLM client
        api_key = "AIzaSyAYY4TTtVcOjisOt6nFcx0xppSyBCUKayo"
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=input_data,
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                max_output_tokens=3000,
                temperature=0.3,
                response_mime_type='application/json',
                response_schema=JobAssessmentOutput,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error assessing job match: {str(e)}"

class JobAssessmentTool(BaseTool):
    """Tool for assessing the candidate's fit for a job offer"""
    name: str = "assess_job_match"
    description: str = "Assesses the candidate's fit for a job offer based on their profile"
    args_schema: Type[BaseModel] = JobAssessmentInput
    return_direct: bool = False
    def _run(self, job_offer: str, user_profile: str) -> str:
        """Synchronous run"""
        return assess_job_match(job_offer, user_profile)
    
    def _arun(self, job_offer: str, user_profile: str) -> str:
        """Async run - just calls sync version"""
        return self._run(job_offer, user_profile)