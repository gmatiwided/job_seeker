"""
Simple test script for CV Generator Agent
Run this to quickly test the agent with a custom job offer
"""

from cv_generator_agent import CVGeneratorAgent, API_KEY
from pathlib import Path


def test_agent(job_offer: str = None):
    """Test the CV generator agent"""
    
    # Default job offer if none provided
    if not job_offer:
        job_offer = """
Data Scientist Position - Junior to Mid Level

We are looking for a passionate Data Scientist to join our team in Tunisia.

Requirements:
- 2+ years of experience in data science or related field
- Strong Python programming skills (pandas, scikit-learn, matplotlib)
- Experience with machine learning and predictive modeling
- SQL and database querying experience
- Data visualization skills (Tableau, Power BI, or similar)
- Strong analytical and problem-solving abilities

Responsibilities:
- Analyze complex datasets to derive actionable insights
- Build and deploy machine learning models
- Create dashboards and visualizations for stakeholders
- Collaborate with cross-functional teams
- Communicate findings to both technical and non-technical audiences

Nice to have:
- Experience with logistics or supply chain analytics
- Knowledge of statistical analysis and hypothesis testing
- Familiarity with Agile methodologies
"""
    
    print("🚀 Initializing CV Generator Agent...\n")
    
    # Initialize agent
    agent = CVGeneratorAgent(api_key=API_KEY)
    
    # Check if profile loaded
    if not agent.user_profile:
        print("❌ Failed to load user profile!")
        return None
    
    print(f"✅ Loaded profile for: {agent.user_profile.get('name', 'Unknown')}\n")
    
    # Generate CV and assessment
    print("⏳ Generating CV and assessment...\n")
    result = agent.generate_cv_for_job(job_offer, verbose=True)
    
    # Save and display
    output_dir = Path("build_with_ai/scripts/output")
    output_dir.mkdir(exist_ok=True)
    
    # Save files
    cv_file = output_dir / "test_cv.txt"
    assessment_file = output_dir / "test_assessment.txt"
    
    with open(cv_file, "w", encoding="utf-8") as f:
        f.write(result.get("cv", "No CV generated"))
    
    with open(assessment_file, "w", encoding="utf-8") as f:
        f.write(result.get("assessment", "No assessment generated"))
    
    # Display results
    print("\n" + "=" * 80)
    print("📊 ASSESSMENT PREVIEW (first 500 chars)")
    print("=" * 80)
    assessment = result.get("assessment", "No assessment generated")
    print(assessment[:500] + "..." if len(assessment) > 500 else assessment)
    
    print("\n" + "=" * 80)
    print("📄 CV PREVIEW (first 500 chars)")
    print("=" * 80)
    cv = result.get("cv", "No CV generated")
    print(cv[:500] + "..." if len(cv) > 500 else cv)
    
    print("\n" + "=" * 80)
    print("💾 SAVED FILES")
    print("=" * 80)
    print(f"📄 CV: {cv_file}")
    print(f"📊 Assessment: {assessment_file}")
    
    print("\n📖 To view full files:")
    print(f"   type {cv_file}")
    print(f"   type {assessment_file}")
    
    return result


if __name__ == "__main__":
    # Run the test
    result = test_agent()
    
    if result:
        print("\n✅ Test completed successfully!")
        print(f"   CV length: {len(result.get('cv', ''))} characters")
        print(f"   Assessment length: {len(result.get('assessment', ''))} characters")
    else:
        print("\n❌ Test failed!")
