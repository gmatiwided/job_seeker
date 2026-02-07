"""
Test script for the Job Seeker Agent
Tests the full workflow: assess → CV → cover letter → interview prep
"""
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from agents.job_seeker import process_job_application


def test_good_match_job():
    """Test with a job that should be a good match"""
    print("\n" + "="*80)
    print("TEST 1: Good Match Job - Should Generate All Materials")
    print("="*80 + "\n")
    
    job_offer = """
Data Scientist
TechCorp Tunisia

We are seeking a talented Data Scientist to join our growing analytics team.

Requirements:
- 2+ years of experience in data science or related field
- Strong proficiency in Python (NumPy, Pandas, Scikit-learn)
- Experience with SQL for data extraction and manipulation
- Knowledge of machine learning algorithms and model deployment
- Experience with data visualization tools (Tableau, Power BI)
- Bachelor's or Master's degree in Computer Science, Statistics, or related field

Responsibilities:
- Build and deploy predictive models to solve business problems
- Analyze large datasets to extract actionable insights
- Create dashboards and reports for stakeholders
- Collaborate with engineering teams to implement ML solutions
- Continuously improve model performance and accuracy

Nice to Have:
- Experience with cloud platforms (AWS, Azure, GCP)
- Knowledge of deep learning frameworks (TensorFlow, PyTorch)
- Experience in logistics or supply chain optimization

Location: Tunis, Tunisia
Type: Full-time
"""
    
    try:
        result = process_job_application(
            job_offer=job_offer,
            job_title="Data Scientist",
            company="TechCorp Tunisia"
        )
        
        print("\n" + "="*80)
        print("📊 RESULTS SUMMARY")
        print("="*80)
        print(f"\n📁 Saved in: {result['folder_name']}")
        print(f"\n✅ Materials Generated:")
        print(f"   - Assessment: {'✓' if result.get('assessment') else '✗'}")
        print(f"   - CV: {'✓' if result.get('cv') else '✗'}")
        print(f"   - Cover Letter: {'✓' if result.get('cover_letter') else '✗'}")
        print(f"   - Interview Prep: {'✓' if result.get('interview_prep') else '✗'}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_poor_match_job():
    """Test with a job that should NOT be a good match"""
    print("\n" + "="*80)
    print("TEST 2: Poor Match Job - Should Stop After Assessment")
    print("="*80 + "\n")
    
    job_offer = """
Senior Backend Engineer (10+ years experience)
MegaCorp International

Requirements:
- 10+ years of professional software engineering experience
- Expert-level knowledge of Java, C++, and distributed systems
- Experience leading teams of 10+ engineers
- Deep expertise in microservices architecture
- PhD in Computer Science preferred
- Experience with high-frequency trading systems

This role requires extensive backend engineering expertise and leadership experience.
"""
    
    try:
        result = process_job_application(
            job_offer=job_offer,
            job_title="Senior Backend Engineer",
            company="MegaCorp"
        )
        
        print("\n" + "="*80)
        print("📊 RESULTS SUMMARY")
        print("="*80)
        print(f"\n📁 Saved in: {result['folder_name']}")
        print(f"\n✅ Materials Generated:")
        print(f"   - Assessment: {'✓' if result.get('assessment') else '✗'}")
        print(f"   - CV: {'✓' if result.get('cv') else '✗'}")
        print(f"   - Cover Letter: {'✓' if result.get('cover_letter') else '✗'}")
        print(f"   - Interview Prep: {'✓' if result.get('interview_prep') else '✗'}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("\n🚀 JOB SEEKER AGENT TEST SUITE")
    print("="*80)
    
    # Test 1: Good match
    result1 = test_good_match_job()
    
    # Wait a bit between tests
    print("\n" + "."*80)
    print("Waiting between tests...")
    print("."*80)
    
    # Test 2: Poor match
    result2 = test_poor_match_job()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
    print("\nCheck the output folder for generated materials:")
    print(f"  📁 build_with_ai/output/")
