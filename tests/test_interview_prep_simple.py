"""
Simple test script for interview_prep_generator.py
Quick test with minimal setup
"""

import yaml
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.interview_prep_generator import generate_interview_prep_sync


def load_profile() -> str:
    """Load profile from YAML"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


def quick_test():
    """Quick test of interview prep generation"""
    
    print("🚀 Quick Interview Prep Generator Test\n")
    
    # Simple materials
    job_offer = """
Data Scientist Position
Company: TechCorp Tunisia
Requirements: Python, ML, SQL, 2+ years experience
Responsibilities: Build models, analyze data
"""
    
    cv = """
AMINA BEN YOUSSEF
Data Scientist

EXPERIENCE:
Junior Data Scientist - SmartLogix (2 years)
- Built predictive model improving efficiency by 12%
- Created dashboards using Tableau

SKILLS:
Python, SQL, Machine Learning, Data Visualization
"""
    
    cover_letter = """
I am excited to apply for the Data Scientist position.
My 2 years of Python experience and proven track record
make me a strong candidate.
"""
    
    assessment = """
Match Score: 85/100
Strong match with relevant skills and experience.
"""
    
    # Generate interview prep
    print("📋 Preparing interview materials...\n")
    print("⏳ Generating interview preparation guide...")
    print("   (This may take 30-60 seconds...)\n")
    
    interview_prep = generate_interview_prep_sync(
        job_offer=job_offer,
        cv_content=cv,
        cover_letter=cover_letter,
        job_assessment=assessment
    )
    
    # Display result
    if interview_prep and not interview_prep.startswith("Error"):
        print("✅ Interview Preparation Guide Generated!\n")
        print("=" * 70)
        print(interview_prep)
        print("=" * 70)
        
        # Save to central output folder as markdown
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "quick_test_interview_prep.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(interview_prep)
        
        # Stats
        word_count = len(interview_prep.split())
        line_count = len(interview_prep.splitlines())
        
        print(f"\n📊 Statistics:")
        print(f"   💾 Saved to: {output_file}")
        print(f"   📏 Words: {word_count:,}")
        print(f"   📄 Lines: {line_count:,}")
        print(f"   📝 Characters: {len(interview_prep):,}")
        
        # Check for key sections
        has_questions = "QUESTION" in interview_prep
        has_answers = "ANSWER" in interview_prep
        has_assessment = "SELF-ASSESSMENT" in interview_prep
        has_star = "STAR" in interview_prep
        has_scoring = "Score yourself" in interview_prep or "1-5" in interview_prep
        
        print(f"\n✓ Content Verification:")
        print(f"   Questions Present: {'✓' if has_questions else '✗'}")
        print(f"   Model Answers: {'✓' if has_answers else '✗'}")
        print(f"   Self-Assessment: {'✓' if has_assessment else '✗'}")
        print(f"   STAR Method: {'✓' if has_star else '✗'}")
        print(f"   Scoring Rubric: {'✓' if has_scoring else '✗'}")
        
        # Count sections
        question_count = interview_prep.count("QUESTION")
        
        print(f"\n📋 Content Summary:")
        print(f"   Total Questions: ~{question_count}")
        print(f"   Includes: Technical, Behavioral, Situational questions")
        print(f"   Plus: Self-assessment criteria and improvement tips")
        
        print(f"\n🎯 Use this guide to:")
        print(f"   1. Practice answering interview questions")
        print(f"   2. Self-assess your responses (1-5 scale)")
        print(f"   3. Learn what makes answers effective")
        print(f"   4. Identify areas for improvement")
        
    else:
        print(f"❌ Error: {interview_prep}")


if __name__ == "__main__":
    quick_test()
