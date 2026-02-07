"""
Simple quick test for Job Seeker Agent
Tests with one good match job
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from agents.job_seeker import process_job_application


def main():
    print("🚀 Quick Job Seeker Agent Test\n")
    
    job_offer = """
Junior Data Scientist
DataCo Tunisia

Requirements:
- 2+ years experience with Python, SQL, Machine Learning
- Experience building predictive models
- Data visualization skills (Tableau preferred)
- Bachelor's degree in related field

Responsibilities:
- Build ML models for business optimization
- Create dashboards and reports
- Analyze data to drive insights
"""
    
    print("📋 Processing job application...")
    print("-" * 60)
    
    result = process_job_application(
        job_offer=job_offer,
        job_title="Junior Data Scientist",
        company="DataCo"
    )
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    print(f"\n📁 Folder: {result['folder_name']}")
    print(f"\n✅ Generated:")
    print(f"   Assessment: {'✓' if result.get('assessment') else '✗'}")
    print(f"   CV: {'✓' if result.get('cv') else '✗'}")
    print(f"   Cover Letter: {'✓' if result.get('cover_letter') else '✗'}")
    print(f"   Interview Prep: {'✓' if result.get('interview_prep') else '✗'}")
    print(f"\n💾 All files saved in: {result['job_folder']}")


if __name__ == "__main__":
    try:
        main()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
