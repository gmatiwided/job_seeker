"""
Test script for job_assessment_tool.py
Tests the job assessment functionality
"""

import yaml
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.job_assessment_tool import JobAssessmentTool, assess_job_match


def load_profile() -> str:
    """Load profile from YAML and convert to string"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


# Test job offers
JOB_OFFER_PERFECT_MATCH = """
Junior Data Scientist

Company: DataTech Tunisia

Requirements:
- 2+ years of experience in data science or analytics
- Strong Python skills (pandas, scikit-learn, matplotlib)
- SQL and database experience
- Machine learning knowledge (regression, classification, clustering)
- Data visualization with Tableau or Power BI
- Agile methodology experience
- Master's degree in Data Science or related field

Nice to Have:
- Logistics or supply chain experience
- R programming
- Git and Jupyter Notebooks

Responsibilities:
- Build predictive models
- Create dashboards and visualizations
- Collaborate with cross-functional teams
- Present findings to stakeholders

Location: Tunisia
"""

JOB_OFFER_STRETCH_ROLE = """
Senior Data Scientist - Machine Learning Lead

Company: AI Innovations

Requirements:
- 5+ years in data science and ML
- Expert Python and deep learning (TensorFlow, PyTorch)
- Experience leading data science teams
- Production ML deployment experience
- PhD or Master's in Computer Science/Statistics
- Published research papers

Responsibilities:
- Lead ML engineering team
- Design scalable ML architectures
- Mentor junior data scientists
- Research cutting-edge techniques

Location: Remote
Salary: Senior level compensation
"""

JOB_OFFER_MODERATE_MATCH = """
Data Analyst - Business Intelligence

Company: RetailCorp

Requirements:
- 1-3 years of analytics experience
- SQL and data querying
- Excel and data manipulation
- Tableau or Power BI
- Basic statistical knowledge
- Bachelor's degree

Responsibilities:
- Create reports and dashboards
- Analyze sales and operations data
- Support business decisions with data
- Present insights to management

Location: Hybrid
"""


def test_perfect_match():
    """Test with a job that's a strong match"""
    print("=" * 80)
    print("TEST 1: Perfect Match Job Offer")
    print("=" * 80)
    
    profile = load_profile()
    
    print("\n⏳ Assessing job match...")
    result = assess_job_match(JOB_OFFER_PERFECT_MATCH, profile)
    
    if result and not result.startswith("Error"):
        print("✅ Assessment completed\n")
        
        # Parse JSON result
        try:
            assessment_data = json.loads(result)
            
            print("📊 MATCH SCORE:", assessment_data.get('match_score', 'N/A'))
            print("\n📝 ASSESSMENT:")
            print(assessment_data.get('assessment', 'N/A'))
            
            print("\n💪 STRENGTHS:")
            for i, strength in enumerate(assessment_data.get('strengths', []), 1):
                print(f"  {i}. {strength}")
            
            print("\n⚠️  GAPS:")
            gaps = assessment_data.get('gaps', [])
            if gaps:
                for i, gap in enumerate(gaps, 1):
                    print(f"  {i}. {gap}")
            else:
                print("  None significant")
            
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(assessment_data.get('recommendations', []), 1):
                print(f"  {i}. {rec}")
            
            # Save to file
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "test_assessment_perfect_match.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(assessment_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saved to: {output_file}")
            
            return assessment_data
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print("Raw result:", result[:200])
            return None
    else:
        print(f"❌ Error: {result}")
        return None


def test_stretch_role():
    """Test with a job that's a stretch/reach"""
    print("\n\n" + "=" * 80)
    print("TEST 2: Stretch Role (Senior Position)")
    print("=" * 80)
    
    profile = load_profile()
    
    print("\n⏳ Assessing job match...")
    result = assess_job_match(JOB_OFFER_STRETCH_ROLE, profile)
    
    if result and not result.startswith("Error"):
        print("✅ Assessment completed\n")
        
        try:
            assessment_data = json.loads(result)
            
            print("📊 MATCH SCORE:", assessment_data.get('match_score', 'N/A'))
            print("\n📝 ASSESSMENT:")
            print(assessment_data.get('assessment', 'N/A'))
            
            print("\n💪 STRENGTHS:")
            for i, strength in enumerate(assessment_data.get('strengths', []), 1):
                print(f"  {i}. {strength}")
            
            print("\n⚠️  GAPS:")
            for i, gap in enumerate(assessment_data.get('gaps', []), 1):
                print(f"  {i}. {gap}")
            
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(assessment_data.get('recommendations', []), 1):
                print(f"  {i}. {rec}")
            
            # Save to file
            output_dir = Path(__file__).parent.parent / "output"
            output_file = output_dir / "test_assessment_stretch_role.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(assessment_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saved to: {output_file}")
            
            return assessment_data
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON")
            return None
    else:
        print(f"❌ Error: {result}")
        return None


def test_moderate_match():
    """Test with a moderate match job"""
    print("\n\n" + "=" * 80)
    print("TEST 3: Moderate Match (Data Analyst)")
    print("=" * 80)
    
    profile = load_profile()
    
    print("\n⏳ Assessing job match...")
    result = assess_job_match(JOB_OFFER_MODERATE_MATCH, profile)
    
    if result and not result.startswith("Error"):
        print("✅ Assessment completed\n")
        
        try:
            assessment_data = json.loads(result)
            
            print("📊 MATCH SCORE:", assessment_data.get('match_score', 'N/A'))
            print("\n📝 ASSESSMENT:")
            print(assessment_data.get('assessment', 'N/A'))
            
            print("\n💪 STRENGTHS:")
            for i, strength in enumerate(assessment_data.get('strengths', []), 1):
                print(f"  {i}. {strength}")
            
            print("\n⚠️  GAPS:")
            gaps = assessment_data.get('gaps', [])
            if gaps:
                for i, gap in enumerate(gaps, 1):
                    print(f"  {i}. {gap}")
            else:
                print("  Candidate may be overqualified")
            
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(assessment_data.get('recommendations', []), 1):
                print(f"  {i}. {rec}")
            
            # Save to file
            output_dir = Path(__file__).parent.parent / "output"
            output_file = output_dir / "test_assessment_moderate_match.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(assessment_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saved to: {output_file}")
            
            return assessment_data
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON")
            return None
    else:
        print(f"❌ Error: {result}")
        return None


def test_tool_class():
    """Test the JobAssessmentTool class"""
    print("\n\n" + "=" * 80)
    print("TEST 4: JobAssessmentTool Class")
    print("=" * 80)
    
    tool = JobAssessmentTool()
    
    print(f"\n🔧 Tool initialized")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    
    profile = load_profile()
    
    print("\n⏳ Running tool...")
    result = tool._run(JOB_OFFER_PERFECT_MATCH, profile)
    
    if result and not result.startswith("Error"):
        print("✅ Tool executed successfully")
        
        try:
            assessment_data = json.loads(result)
            print(f"📊 Match Score: {assessment_data.get('match_score', 'N/A')}")
            print(f"💪 Strengths Count: {len(assessment_data.get('strengths', []))}")
            print(f"⚠️  Gaps Count: {len(assessment_data.get('gaps', []))}")
            print(f"💡 Recommendations Count: {len(assessment_data.get('recommendations', []))}")
            return True
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON")
            return False
    else:
        print(f"❌ Tool failed: {result}")
        return False


def compare_assessments():
    """Compare all assessment scores"""
    print("\n\n" + "=" * 80)
    print("ASSESSMENT COMPARISON")
    print("=" * 80)
    
    output_dir = Path(__file__).parent.parent / "output"
    assessment_files = list(output_dir.glob("test_assessment_*.json"))
    
    if not assessment_files:
        print("⚠️ No assessment files found!")
        return
    
    print("\n📊 Score Comparison:\n")
    
    scores = []
    for file in sorted(assessment_files):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        job_type = file.stem.replace('test_assessment_', '').replace('_', ' ').title()
        score = data.get('match_score', 0)
        scores.append((job_type, score))
        
        print(f"  {job_type:.<40} {score:.1f}/100")
    
    print("\n📈 Score Range:")
    if scores:
        min_score = min(s[1] for s in scores)
        max_score = max(s[1] for s in scores)
        print(f"  Lowest:  {min_score:.1f}/100")
        print(f"  Highest: {max_score:.1f}/100")
        print(f"  Range:   {max_score - min_score:.1f} points")


def main():
    """Run all tests"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 22 + "JOB ASSESSMENT TOOL TEST SUITE" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    
    results = []
    
    # Test 1: Perfect match
    result1 = test_perfect_match()
    results.append(("Perfect Match Assessment", result1 is not None))
    
    # Test 2: Stretch role
    result2 = test_stretch_role()
    results.append(("Stretch Role Assessment", result2 is not None))
    
    # Test 3: Moderate match
    result3 = test_moderate_match()
    results.append(("Moderate Match Assessment", result3 is not None))
    
    # Test 4: Tool class
    result4 = test_tool_class()
    results.append(("Tool Class Test", result4))
    
    # Compare assessments
    compare_assessments()
    
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
    print("\n💡 To view assessment files:")
    print(f"   type {output_dir}\\test_assessment_perfect_match.json")


if __name__ == "__main__":
    main()
