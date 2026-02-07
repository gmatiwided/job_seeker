"""
Interview Preparation Generator Tool
Generates mock interview questions, answers, and self-assessment guide using Google GenAI
"""

from pydantic import BaseModel, Field
from langchain_core.tools import tool, BaseTool
from google import genai
from google.genai import types
from typing import Type


class InterviewPrepInput(BaseModel):
    """Input schema for interview preparation generation"""
    job_offer: str = Field(description="The job offer description with requirements and responsibilities")
    cv_content: str = Field(description="The candidate's CV content")
    cover_letter: str = Field(description="The candidate's cover letter")
    job_assessment: str = Field(description="Job assessment with match score and analysis")


def generate_interview_prep_sync(
    job_offer: str, 
    cv_content: str, 
    cover_letter: str, 
    job_assessment: str
) -> str:
    """
    Generates comprehensive interview preparation materials including questions, answers, 
    explanations, and self-assessment guide.
    Synchronous version - no async/await needed.
    
    Args:
        job_offer: The job offer description
        cv_content: Candidate's CV text
        cover_letter: Candidate's cover letter text
        job_assessment: Job match assessment
        
    Returns:
        Interview preparation guide in markdown format
    """
    prompt = """You are an expert interview coach and career consultant with deep knowledge of technical interviews, behavioral assessments, and hiring best practices across various industries.

Your task is to create a comprehensive interview preparation guide in MARKDOWN FORMAT that helps candidates practice and self-assess their readiness for a specific job interview.

IMPORTANT: Use proper markdown formatting throughout:
- Use # for main headers, ## for sections, ### for subsections
- Use **bold** for emphasis
- Use - or * for bullet lists
- Use numbered lists where appropriate
- Use > for blockquotes
- Use ``` for code blocks if needed
- Use --- for horizontal rules
- Use tables where appropriate
- Use checkboxes [ ] for checklists

CRITICAL OBJECTIVES:

1. Generate 8-10 interview questions focused on:
   - 5-6 Technical questions (primary focus - based on job requirements and CV skills)
   - 2-3 Behavioral questions (brief, STAR format)
   - 1-2 Role fit questions

2. THREE-PART STRUCTURE (strictly follow):
   
   **PART 1: Interview Overview**
   - Expected Interview Format (2-3 bullets)
   - Profile Strengths (3 bullets max)
   - Areas to Prepare Extra (2 bullets max)
   
   **PART 2: Questions**
   - List ALL questions together
   - Number them clearly (Q1, Q2, etc.)
   - No answers here, just questions
   
   **PART 3: Answers**
   - Provide answer for each question
   - Keep answers SHORT: 60-100 words
   - Focus on practical, CV-based responses

3. Keep EVERYTHING concise:
   - Part 1: 150-200 words total
   - Part 2: Just the questions
   - Part 3: 60-100 words per answer
   - Total guide: 1,500-2,000 words maximum

4. Technical focus:
   - Questions should relate to job requirements AND CV experience
   - Test actual skills mentioned in CV
   - Be specific to the role (Python, ML, SQL, etc.)
   - Practical, not theoretical

INTERVIEW QUESTION GUIDELINES:

Generate 8-10 questions total with emphasis on technical:

**Technical Questions (5-6 questions):**
- Focus on skills mentioned in both job description AND CV
- Example topics: Python, SQL, ML algorithms, data visualization
- Test practical application, not just theory
- Relate to specific projects or achievements from CV

**Behavioral Questions (2-3 questions):**
- Focus on achievements mentioned in CV
- Use STAR format for answers
- Keep brief and focused

**Role Fit Questions (1-2 questions):**
- Why this role/company
- Career goals

Questions should be:
- Specific to the job requirements
- Related to candidate's CV experience
- Realistic and commonly asked
- Appropriate for seniority level

OUTPUT STRUCTURE (IN MARKDOWN) - EXACTLY 3 PARTS:

# 🎯 Interview Preparation Guide

**Candidate:** [Name]  
**Position:** [Job Title]  
**Company:** [Company Name]

---

## Part 1: Interview Overview

### 📋 Expected Interview Format
- [Type: Phone/Video/In-person]
- [Duration and structure]
- [Key focus areas from job description]

### 💪 Your Profile Strengths
1. [Strength 1 with brief relevance]
2. [Strength 2 with brief relevance]
3. [Strength 3 with brief relevance]

### ⚠️ Areas to Prepare Extra
1. [Gap/Area 1 - how to address]
2. [Gap/Area 2 - how to address]

---

## Part 2: Interview Questions

### Technical Questions

**Q1.** [Technical question about specific skill from job/CV]

**Q2.** [Technical question about tool/technology]

**Q3.** [Technical question about methodology/approach]

**Q4.** [Technical question about problem-solving]

**Q5.** [Technical question about specific achievement from CV]

**Q6.** [Technical question if needed]

### Behavioral Questions

**Q7.** [Behavioral question about teamwork/achievement]

**Q8.** [Behavioral question about challenge/learning]

**Q9.** [Behavioral question if needed]

### Role Fit Questions

**Q10.** [Why this role/company]

---

## Part 3: Model Answers

### Answer to Q1
[Concise answer: 60-100 words]
[Based on CV experience]
[Practical and specific]

### Answer to Q2
[Concise answer: 60-100 words]

### Answer to Q3
[Concise answer: 60-100 words]

### Answer to Q4
[Concise answer: 60-100 words]

### Answer to Q5
[Concise answer: 60-100 words]

### Answer to Q6
[Concise answer if applicable]

### Answer to Q7 (Behavioral - STAR)
**Situation:** [1 sentence]  
**Task:** [1 sentence]  
**Action:** [2 sentences]  
**Result:** [1 sentence with metric]

### Answer to Q8 (Behavioral - STAR)
[Same STAR format, brief]

### Answer to Q9
[If applicable]

### Answer to Q10
[Brief, genuine response: 60-80 words]

---

**Practice Tips:**
- Review questions without looking at answers first
- Practice answers out loud
- Time yourself (2-3 minutes per answer)
- Focus on being clear and concise

**Good luck! 🎯**

---

CRITICAL FORMATTING RULES:
1. Exactly 3 parts: Overview → Questions → Answers
2. Technical questions are the priority (5-6 out of 8-10 total)
3. Keep Part 1 under 200 words
4. List ALL questions together in Part 2
5. All answers in Part 3, each 60-100 words
6. Total guide: 1,500-2,000 words maximum
7. No additional sections or explanations

CRITICAL RULES FOR GENERATING CONTENT:

1. AUTHENTICITY
   - All answers MUST be based on actual experiences from CV
   - Don't invent projects, achievements, or skills not in profile
   - Use real examples with real outcomes

2. RELEVANCE
   - Connect every answer to job requirements
   - Use keywords from job description naturally
   - Show understanding of role responsibilities

3. STAR METHOD (for behavioral only)
   - Keep it brief: 1 sentence each for S, T, R and 2 for A
   - Use "I", not "we"
   - Result should have metric when possible

4. TECHNICAL FOCUS
   - Questions should test actual CV skills against job requirements
   - No theoretical questions - practical application only
   - Reference specific technologies/tools from CV and job"""

    input_data = f"""INPUT DATA:

Job Offer:
{job_offer}

Candidate's CV:
{cv_content}

Cover Letter:
{cover_letter}

Job Assessment:
{job_assessment}

Please generate a comprehensive interview preparation guide following the structure above. 
Base all questions and answers on the candidate's actual background. Make it practical, 
actionable, and empowering for self-assessment."""

    try:
        # Get unified LLM client
        api_key = "AIzaSyAYY4TTtVcOjisOt6nFcx0xppSyBCUKayo"
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=input_data,
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                max_output_tokens=9000,  # Reduced for shorter, focused output
                temperature=0.7,
            ),
        )

        return response.text
    except Exception as e:
        return f"Error generating interview preparation: {str(e)}"


@tool("generate_interview_prep", return_direct=False)
def generate_interview_prep_tool(
    job_offer: str, 
    cv_content: str, 
    cover_letter: str, 
    job_assessment: str
) -> str:
    """
    Generates comprehensive interview preparation materials including mock questions,
    model answers, explanations, and self-assessment guide.
    
    Args:
        job_offer: The job offer description
        cv_content: Candidate's CV text
        cover_letter: Candidate's cover letter text
        job_assessment: Job match assessment
        
    Returns:
        Interview preparation guide in markdown format
    """
    return generate_interview_prep_sync(job_offer, cv_content, cover_letter, job_assessment)


class InterviewPrepTool(BaseTool):
    """
    LangChain tool for generating interview preparation materials.
    Synchronous implementation - no async needed.
    """
    name: str = "generate_interview_prep"
    description: str = "Generates comprehensive interview preparation guide with mock questions, model answers, explanations, and self-assessment criteria."
    args_schema: Type[BaseModel] = InterviewPrepInput
    return_direct: bool = False
    
    def _run(
        self, 
        job_offer: str, 
        cv_content: str, 
        cover_letter: str, 
        job_assessment: str
    ) -> str:
        """Synchronous run"""
        return generate_interview_prep_sync(job_offer, cv_content, cover_letter, job_assessment)
    
    def _arun(
        self, 
        job_offer: str, 
        cv_content: str, 
        cover_letter: str, 
        job_assessment: str
    ) -> str:
        """Async run - just calls sync version"""
        return self._run(job_offer, cv_content, cover_letter, job_assessment)
