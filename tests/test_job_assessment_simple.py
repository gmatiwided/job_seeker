"""
Simple test script for job_assessment_tool.py
Quick test with minimal setup
"""

import yaml
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.job_assessment_tool import assess_job_match


def load_profile() -> str:
    """Load profile from YAML"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


def quick_test():
    """Quick test of job assessment"""
    
    print("🚀 Quick Job Assessment Test\n")
    
    # Simple job offer
    job_offer = """
Data Scientist - Junior Position

Requirements:
- 2+ years experience in data science
- Python (pandas, scikit-learn)
- SQL and data analysis
- Machine learning knowledge
- Data visualization skills
- Bachelor's or Master's degree

Responsibilities:
- Build predictive models
- Analyze data and create insights
- Work with cross-functional teams

Location: Tunisia
"""
    
    # Load profile
    print("📋 Loading profile...")
    profile = load_profile()
    print(f"✅ Profile loaded ({len(profile)} chars)\n")
    
    # Assess job match
    print("⏳ Assessing job match...")
    result = assess_job_match(job_offer, profile)
    
    # Display result
    if result and not result.startswith("Error"):
        print("✅ Assessment Complete!\n")
        
        try:
            assessment = json.loads(result)
            
            print("=" * 60)
            print("📊 JOB MATCH ASSESSMENT")
            print("=" * 60)
            
            print(f"\n🎯 MATCH SCORE: {assessment.get('match_score', 'N/A')}/100")
            
            print(f"\n📝 ASSESSMENT:")
            print(f"   {assessment.get('assessment', 'N/A')}")
            
            print(f"\n💪 STRENGTHS:")
            for i, strength in enumerate(assessment.get('strengths', []), 1):
                print(f"   {i}. {strength}")
            
            print(f"\n⚠️  GAPS:")
            gaps = assessment.get('gaps', [])
            if gaps:
                for i, gap in enumerate(gaps, 1):
                    print(f"   {i}. {gap}")
            else:
                print("   None - Excellent match!")
            
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(assessment.get('recommendations', []), 1):
                print(f"   {i}. {rec}")
            
            print("\n" + "=" * 60)
            
            # Save to central output folder
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "quick_test_assessment.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(assessment, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saved to: {output_file}")
            print(f"📏 Match Score: {assessment.get('match_score', 0)}/100")
            
            # Score interpretation
            score = assessment.get('match_score', 0)
            if score >= 90:
                interpretation = "🌟 Exceptional Match"
            elif score >= 80:
                interpretation = "✨ Strong Match"
            elif score >= 70:
                interpretation = "👍 Good Match"
            elif score >= 60:
                interpretation = "🤔 Moderate Match"
            else:
                interpretation = "⚠️  Weak Match"
            
            print(f"📈 Interpretation: {interpretation}")
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print("Raw result:", result[:500])
    else:
        print(f"❌ Error: {result}")


if __name__ == "__main__":
    quick_test()
