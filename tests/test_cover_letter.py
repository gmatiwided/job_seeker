"""
Test script for cover_letter_generator.py
Tests the cover letter generation functionality with various job scenarios
"""

import yaml
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.cover_letter_generator import CoverLetterGeneratorTool, generate_cover_letter_sync
from tools.job_assessment_tool import assess_job_match


def load_profile() -> str:
    """Load profile from YAML and convert to string"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


# Test job offers
JOB_OFFER_JUNIOR_DS = """
Junior Data Scientist

Company: DataTech Tunisia
Location: Tunis, Tunisia (Hybrid)

About Us:
DataTech Tunisia is a leading analytics consultancy helping businesses make data-driven decisions.

Position Overview:
We're seeking a Junior Data Scientist to join our growing team and work on exciting projects
in logistics and operational analytics.

Requirements:
- 2+ years of experience in data science or analytics
- Strong Python skills (pandas, scikit-learn, matplotlib)
- SQL and database experience
- Machine learning knowledge (regression, classification, clustering)
- Data visualization with Tableau or Power BI
- Master's degree in Data Science or related field
- Excellent communication skills

Nice to Have:
- Logistics or supply chain analytics experience
- R programming
- Git and Jupyter Notebooks
- Experience with Agile methodologies

Responsibilities:
- Build and deploy predictive models for business optimization
- Create interactive dashboards and visualizations
- Collaborate with cross-functional teams
- Present insights to both technical and non-technical stakeholders
- Contribute to data strategy and best practices

What We Offer:
- Competitive salary
- Professional development opportunities
- Collaborative work environment
- Hybrid work arrangement

To Apply:
Send your CV and cover letter to careers@datatech-tunisia.com
"""

JOB_OFFER_SENIOR_ANALYST = """
Senior Data Analyst

Company: AI Innovations Ltd
Location: Remote

We're looking for a Senior Data Analyst with 5+ years of experience to lead
our analytics initiatives.

Requirements:
- 5+ years in data analysis
- Expert SQL and Python
- Business intelligence tools
- Team leadership experience
- Bachelor's degree required

Responsibilities:
- Lead analytics team
- Develop BI strategy
- Mentor junior analysts
"""


def test_junior_ds_position():
    """Test with junior data scientist position"""
    print("=" * 80)
    print("TEST 1: Junior Data Scientist Position")
    print("=" * 80)
    
    profile = load_profile()
    
    # First get job assessment
    print("\n📊 Step 1: Assessing job match...")
    assessment = assess_job_match(JOB_OFFER_JUNIOR_DS, profile)
    
    try:
        assessment_data = json.loads(assessment)
        match_score = assessment_data.get('match_score', 0)
        print(f"✅ Assessment complete - Match Score: {match_score}/100")
    except:
        print("✅ Assessment complete")
    
    # Generate cover letter
    print("\n📝 Step 2: Generating cover letter...")
    cover_letter = generate_cover_letter_sync(
        job_offer=JOB_OFFER_JUNIOR_DS,
        user_profile=profile,
        job_assessment=assessment
    )
    
    if cover_letter and not cover_letter.startswith("Error"):
        print(f"✅ Cover letter generated ({len(cover_letter)} characters)\n")
        
        # Display cover letter
        print("=" * 80)
        print("GENERATED COVER LETTER")
        print("=" * 80)
        print(cover_letter)
        print("=" * 80)
        
        # Save to file
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        cover_letter_file = output_dir / "test_cover_letter_junior_ds.txt"
        with open(cover_letter_file, "w", encoding="utf-8") as f:
            f.write(cover_letter)
        
        print(f"\n💾 Saved to: {cover_letter_file}")
        
        # Analysis
        word_count = len(cover_letter.split())
        line_count = len(cover_letter.splitlines())
        
        print(f"\n📊 Cover Letter Analysis:")
        print(f"   Words: {word_count}")
        print(f"   Lines: {line_count}")
        print(f"   Characters: {len(cover_letter)}")
        
        # Check for key elements
        has_contact = "Email" in cover_letter or "@" in cover_letter
        has_position = "Data Scientist" in cover_letter
        has_company = "DataTech" in cover_letter
        has_closing = "Sincerely" in cover_letter or "Best regards" in cover_letter
        
        print(f"\n✓ Quality Checks:")
        print(f"   Contact Info: {'✓' if has_contact else '✗'}")
        print(f"   Position Name: {'✓' if has_position else '✗'}")
        print(f"   Company Name: {'✓' if has_company else '✗'}")
        print(f"   Professional Closing: {'✓' if has_closing else '✗'}")
        
        return cover_letter
    else:
        print(f"❌ Error: {cover_letter}")
        return None


def test_senior_analyst_position():
    """Test with senior analyst position (stretch role)"""
    print("\n\n" + "=" * 80)
    print("TEST 2: Senior Analyst Position (Stretch Role)")
    print("=" * 80)
    
    profile = load_profile()
    
    # Get assessment
    print("\n📊 Step 1: Assessing job match...")
    assessment = assess_job_match(JOB_OFFER_SENIOR_ANALYST, profile)
    
    try:
        assessment_data = json.loads(assessment)
        match_score = assessment_data.get('match_score', 0)
        print(f"✅ Assessment complete - Match Score: {match_score}/100")
    except:
        print("✅ Assessment complete")
    
    # Generate cover letter
    print("\n📝 Step 2: Generating cover letter...")
    cover_letter = generate_cover_letter_sync(
        job_offer=JOB_OFFER_SENIOR_ANALYST,
        user_profile=profile,
        job_assessment=assessment
    )
    
    if cover_letter and not cover_letter.startswith("Error"):
        print(f"✅ Cover letter generated ({len(cover_letter)} characters)\n")
        
        # Save to file
        output_dir = Path(__file__).parent.parent / "output"
        cover_letter_file = output_dir / "test_cover_letter_senior_analyst.txt"
        
        with open(cover_letter_file, "w", encoding="utf-8") as f:
            f.write(cover_letter)
        
        print(f"💾 Saved to: {cover_letter_file}")
        
        # Show preview
        print("\n📄 Preview (first 500 characters):")
        print("-" * 80)
        print(cover_letter[:500] + "..." if len(cover_letter) > 500 else cover_letter)
        print("-" * 80)
        
        return cover_letter
    else:
        print(f"❌ Error: {cover_letter}")
        return None


def test_tool_class():
    """Test the CoverLetterGeneratorTool class"""
    print("\n\n" + "=" * 80)
    print("TEST 3: CoverLetterGeneratorTool Class")
    print("=" * 80)
    
    tool = CoverLetterGeneratorTool()
    
    print(f"\n🔧 Tool initialized")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description[:80]}...")
    
    profile = load_profile()
    
    # Simple assessment for testing
    simple_assessment = "Good match. Candidate has relevant skills and 2 years experience."
    
    print("\n⏳ Running tool...")
    result = tool._run(
        job_offer=JOB_OFFER_JUNIOR_DS,
        user_profile=profile,
        job_assessment=simple_assessment
    )
    
    if result and not result.startswith("Error"):
        print(f"✅ Tool executed successfully")
        print(f"   Generated: {len(result)} characters")
        print(f"   Words: {len(result.split())}")
        
        # Save
        output_dir = Path(__file__).parent.parent / "output"
        output_file = output_dir / "test_cover_letter_tool.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"   Saved to: {output_file}")
        
        return True
    else:
        print(f"❌ Tool failed: {result[:100]}...")
        return False


def compare_cover_letters():
    """Compare all generated cover letters"""
    print("\n\n" + "=" * 80)
    print("COVER LETTER COMPARISON")
    print("=" * 80)
    
    output_dir = Path(__file__).parent.parent / "output"
    letter_files = list(output_dir.glob("test_cover_letter_*.txt"))
    
    if not letter_files:
        print("⚠️ No cover letter files found!")
        return
    
    print(f"\n📊 Found {len(letter_files)} cover letters:\n")
    
    for letter_file in sorted(letter_files):
        with open(letter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        job_type = letter_file.stem.replace('test_cover_letter_', '').replace('_', ' ').title()
        word_count = len(content.split())
        
        print(f"📄 {job_type}")
        print(f"   Words: {word_count}")
        print(f"   Characters: {len(content)}")
        print(f"   Lines: {len(content.splitlines())}")
        print(f"   File: {letter_file.name}")
        print()


def main():
    """Run all tests"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "COVER LETTER GENERATOR TEST SUITE" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    
    results = []
    
    # Test 1: Junior DS position
    result1 = test_junior_ds_position()
    results.append(("Junior DS Cover Letter", result1 is not None))
    
    # Test 2: Senior analyst (stretch)
    result2 = test_senior_analyst_position()
    results.append(("Senior Analyst Cover Letter", result2 is not None))
    
    # Test 3: Tool class
    result3 = test_tool_class()
    results.append(("Tool Class Test", result3))
    
    # Compare outputs
    compare_cover_letters()
    
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
    print("\n💡 To view a cover letter:")
    print(f"   type {output_dir}\\test_cover_letter_junior_ds.txt")


if __name__ == "__main__":
    main()
