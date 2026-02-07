"""
Test script for interview_prep_generator.py
Tests the interview preparation generation functionality
"""

import yaml
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.interview_prep_generator import InterviewPrepTool, generate_interview_prep_sync
from tools.job_assessment_tool import assess_job_match
from tools.cv_generator import generate_cv_sync
from tools.cover_letter_generator import generate_cover_letter_sync


def load_profile() -> str:
    """Load profile from YAML"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


JOB_OFFER = """
Junior Data Scientist

Company: DataTech Tunisia
Location: Tunis, Tunisia (Hybrid - 3 days office, 2 days remote)

About DataTech Tunisia:
We are a fast-growing analytics consultancy specializing in logistics and operational 
analytics. Our team of 50+ data professionals serves clients across North Africa and Europe.

Position Overview:
We're seeking a Junior Data Scientist to join our Logistics Analytics team. You'll work 
on predictive modeling, data visualization, and machine learning projects that directly 
impact our clients' operational efficiency.

Requirements:
- 2+ years of experience in data science, analytics, or related field
- Strong proficiency in Python (pandas, scikit-learn, NumPy, matplotlib, seaborn)
- Experience with SQL and database querying (PostgreSQL preferred)
- Knowledge of machine learning algorithms: regression, classification, clustering
- Data visualization skills using Tableau, Power BI, or similar tools
- Strong analytical and problem-solving abilities
- Excellent communication skills for presenting insights to stakeholders
- Experience working in Agile environments
- Master's degree in Data Science, Statistics, Computer Science, or related field

Nice to Have:
- Experience in logistics, supply chain, or operational analytics
- Knowledge of statistical analysis and hypothesis testing
- Familiarity with Git version control and Jupyter Notebooks
- R programming skills
- Experience with cloud platforms (AWS, GCP, Azure)

Responsibilities:
- Build, validate, and deploy predictive models for business optimization
- Analyze large and complex datasets to extract meaningful insights
- Create interactive dashboards and visualizations for stakeholders
- Collaborate with cross-functional teams including engineers and product managers
- Present findings to both technical and non-technical audiences
- Contribute to data strategy and analytics best practices
- Optimize existing models and improve data pipelines
- Participate in code reviews and knowledge sharing sessions

What We Offer:
- Competitive salary package
- Health insurance
- Professional development budget
- Flexible hybrid work arrangement
- Collaborative and innovative work environment
- Opportunity to work on diverse projects across industries
- Mentorship from senior data scientists

Interview Process:
1. Phone screening (30 minutes)
2. Technical interview (1 hour - Python, SQL, ML concepts)
3. Case study presentation (prepare 20-minute presentation)
4. Final interview with team lead (cultural fit and career goals)

To Apply:
Send your CV and cover letter to careers@datatech-tunisia.com
Application deadline: March 1, 2026
"""


def test_complete_workflow():
    """Test complete workflow: assess -> CV -> cover letter -> interview prep"""
    print("=" * 80)
    print("TEST 1: Complete Interview Preparation Workflow")
    print("=" * 80)
    
    profile = load_profile()
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: Job Assessment
    print("\n📊 Step 1: Assessing job match...")
    assessment = assess_job_match(JOB_OFFER, profile)
    
    try:
        assessment_data = json.loads(assessment)
        match_score = assessment_data.get('match_score', 0)
        print(f"✅ Match Score: {match_score}/100")
    except:
        print("✅ Assessment complete")
        assessment_data = {}
    
    # Step 2: Generate CV
    print("\n📄 Step 2: Generating CV...")
    cv = generate_cv_sync(
        job_offer=JOB_OFFER,
        user_profile=profile,
        job_assessment=assessment
    )
    print(f"✅ CV generated ({len(cv)} characters)")
    
    # Save CV
    cv_file = output_dir / "test_interview_prep_cv.txt"
    with open(cv_file, "w", encoding="utf-8") as f:
        f.write(cv)
    
    # Step 3: Generate Cover Letter
    print("\n📝 Step 3: Generating cover letter...")
    cover_letter = generate_cover_letter_sync(
        job_offer=JOB_OFFER,
        user_profile=profile,
        job_assessment=assessment
    )
    print(f"✅ Cover letter generated ({len(cover_letter)} characters)")
    
    # Save cover letter
    cl_file = output_dir / "test_interview_prep_cover_letter.txt"
    with open(cl_file, "w", encoding="utf-8") as f:
        f.write(cover_letter)
    
    # Step 4: Generate Interview Preparation
    print("\n🎯 Step 4: Generating interview preparation guide...")
    interview_prep = generate_interview_prep_sync(
        job_offer=JOB_OFFER,
        cv_content=cv,
        cover_letter=cover_letter,
        job_assessment=assessment
    )
    
    if interview_prep and not interview_prep.startswith("Error"):
        print(f"✅ Interview prep generated ({len(interview_prep)} characters)\n")
        
        # Save interview prep as markdown
        prep_file = output_dir / "test_interview_preparation_guide.md"
        with open(prep_file, "w", encoding="utf-8") as f:
            f.write(interview_prep)
        
        # Analysis
        word_count = len(interview_prep.split())
        line_count = len(interview_prep.splitlines())
        
        print("=" * 80)
        print("INTERVIEW PREPARATION GUIDE PREVIEW")
        print("=" * 80)
        print(interview_prep[:2000])
        print("\n..." + "." * 76 + "...\n")
        print(interview_prep[-1000:])
        print("=" * 80)
        
        print(f"\n📊 Guide Analysis:")
        print(f"   Words: {word_count:,}")
        print(f"   Lines: {line_count:,}")
        print(f"   Characters: {len(interview_prep):,}")
        
        # Check for key sections
        has_technical = "TECHNICAL QUESTIONS" in interview_prep
        has_behavioral = "BEHAVIORAL QUESTIONS" in interview_prep
        has_situational = "SITUATIONAL" in interview_prep
        has_assessment = "SELF-ASSESSMENT" in interview_prep
        has_star = "STAR" in interview_prep
        has_scoring = "SCORE" in interview_prep or "SCORING" in interview_prep
        
        print(f"\n✓ Content Verification:")
        print(f"   Technical Questions: {'✓' if has_technical else '✗'}")
        print(f"   Behavioral Questions: {'✓' if has_behavioral else '✗'}")
        print(f"   Situational Questions: {'✓' if has_situational else '✗'}")
        print(f"   Self-Assessment Guide: {'✓' if has_assessment else '✗'}")
        print(f"   STAR Method: {'✓' if has_star else '✗'}")
        print(f"   Scoring Rubric: {'✓' if has_scoring else '✗'}")
        
        print(f"\n📁 Files Generated:")
        print(f"   CV: {cv_file}")
        print(f"   Cover Letter: {cl_file}")
        print(f"   Interview Prep: {prep_file}")
        
        return interview_prep
    else:
        print(f"❌ Error: {interview_prep}")
        return None


def test_tool_class():
    """Test the InterviewPrepTool class"""
    print("\n\n" + "=" * 80)
    print("TEST 2: InterviewPrepTool Class")
    print("=" * 80)
    
    tool = InterviewPrepTool()
    
    print(f"\n🔧 Tool initialized")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description[:80]}...")
    
    profile = load_profile()
    
    # Generate minimal materials for testing
    print("\n⏳ Preparing test materials...")
    assessment = "Strong match. 85/100 score. Candidate has relevant Python and ML skills."
    cv = "Sample CV content with Python experience and data science background."
    cover_letter = "Sample cover letter expressing interest in the data scientist role."
    
    print("⏳ Running tool...")
    result = tool._run(
        job_offer=JOB_OFFER,
        cv_content=cv,
        cover_letter=cover_letter,
        job_assessment=assessment
    )
    
    if result and not result.startswith("Error"):
        print(f"✅ Tool executed successfully")
        print(f"   Generated: {len(result):,} characters")
        print(f"   Words: {len(result.split()):,}")
        
        # Save
        output_dir = Path(__file__).parent.parent / "output"
        output_file = output_dir / "test_interview_prep_tool.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"   Saved to: {output_file}")
        
        return True
    else:
        print(f"❌ Tool failed: {result[:200]}...")
        return False


def analyze_guide_structure(guide_text: str):
    """Analyze the structure and content of the interview guide"""
    print("\n\n" + "=" * 80)
    print("GUIDE STRUCTURE ANALYSIS")
    print("=" * 80)
    
    # Count question types
    technical_count = guide_text.count("QUESTION") and guide_text.count("TECHNICAL")
    behavioral_count = guide_text.count("STAR FORMAT")
    
    # Count key sections
    sections = [
        "INTERVIEW OVERVIEW",
        "TECHNICAL QUESTIONS",
        "BEHAVIORAL QUESTIONS",
        "SITUATIONAL",
        "COMPANY/ROLE FIT",
        "YOUR QUESTIONS FOR THE INTERVIEWER",
        "SELF-ASSESSMENT GUIDE",
        "PREPARATION CHECKLIST"
    ]
    
    print("\n📋 Section Presence:")
    for section in sections:
        present = section in guide_text
        print(f"   {section}: {'✓' if present else '✗'}")
    
    # Count assessment criteria
    criteria_count = guide_text.count("SELF-ASSESSMENT CRITERIA")
    model_answers = guide_text.count("MODEL ANSWER")
    explanations = guide_text.count("WHY THIS")
    
    print(f"\n📊 Content Metrics:")
    print(f"   Self-Assessment Sections: {criteria_count}")
    print(f"   Model Answers: {model_answers}")
    print(f"   Answer Explanations: {explanations}")
    
    # Check for scoring elements
    has_rubric = "1-5" in guide_text or "Score yourself" in guide_text
    has_tips = "TIPS" in guide_text or "IMPROVEMENT" in guide_text
    has_red_flags = "RED FLAGS" in guide_text or "AVOID" in guide_text
    
    print(f"\n✓ Self-Assessment Elements:")
    print(f"   Scoring Rubric: {'✓' if has_rubric else '✗'}")
    print(f"   Improvement Tips: {'✓' if has_tips else '✗'}")
    print(f"   Red Flags/Pitfalls: {'✓' if has_red_flags else '✗'}")


def main():
    """Run all tests"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 16 + "INTERVIEW PREPARATION GENERATOR TEST SUITE" + " " * 20 + "║")
    print("╚" + "=" * 78 + "╝")
    
    results = []
    
    # Test 1: Complete workflow
    result1 = test_complete_workflow()
    results.append(("Complete Workflow Test", result1 is not None))
    
    if result1:
        # Analyze the guide
        analyze_guide_structure(result1)
    
    # Test 2: Tool class
    result2 = test_tool_class()
    results.append(("Tool Class Test", result2))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    # Show output location
    output_dir = Path(__file__).parent.parent / "output"
    print(f"\n📁 All outputs saved to: {output_dir}")
    print("\n💡 To view the interview preparation guide:")
    print(f"   type {output_dir}\\test_interview_preparation_guide.md")
    print(f"   Or open in markdown viewer for better formatting")
    
    print("\n📚 Guide includes:")
    print("   • Mock interview questions (Technical, Behavioral, Situational)")
    print("   • Model answers based on your CV")
    print("   • Explanations of what makes answers effective")
    print("   • Self-assessment criteria and scoring rubrics")
    print("   • Tips for improvement and common pitfalls")
    print("   • Preparation checklist and practice schedule")


if __name__ == "__main__":
    main()
