"""
Test script for cv_generator.py
Tests the CV generation tool with real profile data
"""

import yaml
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.cv_generator import CVGeneratorTool, generate_cv_sync


def load_profile(profile_path: str = "../config/profile.yaml") -> str:
    """Load user profile from YAML and convert to string"""
    try:
        full_path = Path(__file__).parent / profile_path
        with open(full_path, 'r', encoding='utf-8') as file:
            profile_data = yaml.safe_load(file)
        
        # Convert dict to formatted string
        profile_str = yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)
        return profile_str
    except Exception as e:
        print(f"Error loading profile: {e}")
        return ""


# Sample job offer
SAMPLE_JOB_OFFER = """
Data Scientist - Junior to Mid Level

Company: TechAnalytics Tunisia

We are seeking a talented Data Scientist to join our growing analytics team in Tunisia.

Requirements:
- 2+ years of experience in data science, analytics, or related field
- Strong proficiency in Python (pandas, scikit-learn, NumPy, matplotlib, seaborn)
- Experience with SQL and database querying (PostgreSQL preferred)
- Knowledge of machine learning algorithms including regression, classification, clustering
- Data visualization skills using Tableau, Power BI, or Plotly
- Strong analytical and problem-solving abilities
- Excellent communication skills for presenting insights
- Experience working in Agile environments

Responsibilities:
- Analyze large and complex datasets to extract meaningful insights
- Build, validate, and deploy predictive models for business use cases
- Create interactive dashboards and visualizations for stakeholders
- Collaborate with cross-functional teams including engineers and product managers
- Present findings to both technical and non-technical audiences
- Contribute to data strategy and analytics best practices
- Optimize existing models and improve data pipelines

Nice to Have:
- Experience in logistics, supply chain, or operational analytics
- Knowledge of statistical analysis and hypothesis testing
- Familiarity with Git version control and Jupyter Notebooks
- R programming skills
- Contributions to data science projects or open-source communities
- Master's degree in Data Science, Statistics, or related field

Location: Tunisia (Hybrid - 3 days office, 2 days remote)
Salary: Competitive, based on experience
Start Date: Immediate
"""

# Sample job assessment
SAMPLE_JOB_ASSESSMENT = """
JOB MATCH ASSESSMENT REPORT

Candidate Overview:
- Name: Amina Ben Youssef
- Specialty: Data Scientist
- Seniority Level: Junior
- Years of Experience: ~2 years

Match Analysis:
Based on the candidate's profile, this appears to be a STRONG match for the position.

Strengths:
- Relevant experience in Data Science with 2 years in the field
- Strong technical skills aligned with job requirements (Python, SQL, ML)
- Demonstrated expertise in logistics and supply chain analytics
- Proven track record with measurable achievements (12% efficiency improvement)
- Master's degree in Data Science from Université de Tunis
- Experience with exact tools mentioned: pandas, scikit-learn, Tableau, Power BI
- Agile methodology experience
- Strong collaborative skills demonstrated in cross-functional work

Skills Match:
Technical Skills: Python (pandas, scikit-learn, matplotlib, seaborn), R, SQL, PostgreSQL
Visualization: Tableau, Power BI, Plotly
Machine Learning: Regression, Classification, Clustering, Decision Trees
Workflow: Git, Jupyter Notebooks, Agile methodologies

Key Achievements:
- Developed predictive delivery-time model reducing delays by 12%
- Built interactive dashboards for operations optimization
- Automated data cleaning workflows saving 20+ hours monthly
- Presented insights to leadership influencing operational decisions

Recommendations:
1. Emphasize logistics/supply chain analytics experience (directly relevant)
2. Highlight the 12% efficiency improvement with predictive modeling
3. Showcase dashboard creation and stakeholder communication skills
4. Mention master's degree in Data Science
5. Stress collaborative work with engineers and operations teams

Confidence Level: STRONG - The candidate meets all core requirements and has directly relevant experience.
"""


def test_sync_function():
    """Test the synchronous generate_cv_sync function"""
    print("=" * 80)
    print("TEST 1: Testing synchronous function generate_cv_sync()")
    print("=" * 80)
    
    # Load profile
    print("\n📋 Loading user profile...")
    profile = load_profile()
    
    if not profile:
        print("❌ Failed to load profile!")
        return None
    
    print(f"✅ Profile loaded ({len(profile)} characters)")
    
    # Generate CV
    print("\n⏳ Generating CV...")
    cv = generate_cv_sync(
        job_offer=SAMPLE_JOB_OFFER,
        user_profile=profile,
        job_assessment=SAMPLE_JOB_ASSESSMENT
    )
    
    if cv and not cv.startswith("Error"):
        print(f"✅ CV generated successfully ({len(cv)} characters)")
        
        # Save to file
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        cv_file = output_dir / "test_sync_cv.txt"
        with open(cv_file, "w", encoding="utf-8") as f:
            f.write(cv)
        
        print(f"💾 Saved to: {cv_file}")
        
        # Show preview
        print("\n" + "=" * 80)
        print("CV PREVIEW (first 800 characters)")
        print("=" * 80)
        print(cv[:800])
        if len(cv) > 800:
            print("...")
        
        return cv
    else:
        print(f"❌ Failed to generate CV: {cv}")
        return None


def test_tool_class():
    """Test the CVGeneratorTool class"""
    print("\n\n" + "=" * 80)
    print("TEST 2: Testing CVGeneratorTool class")
    print("=" * 80)
    
    # Initialize tool
    print("\n🔧 Initializing CVGeneratorTool...")
    tool = CVGeneratorTool()
    
    print(f"✅ Tool initialized")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    
    # Load profile
    print("\n📋 Loading user profile...")
    profile = load_profile()
    
    if not profile:
        print("❌ Failed to load profile!")
        return None
    
    print(f"✅ Profile loaded ({len(profile)} characters)")
    
    # Run tool synchronously
    print("\n⏳ Running tool synchronously...")
    
    try:
        cv = tool._run(
            job_offer=SAMPLE_JOB_OFFER,
            user_profile=profile,
            job_assessment=SAMPLE_JOB_ASSESSMENT
        )
        
        if cv and not cv.startswith("Error"):
            print(f"✅ CV generated successfully ({len(cv)} characters)")
            
            # Save to file
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            cv_file = output_dir / "test_tool_cv.txt"
            with open(cv_file, "w", encoding="utf-8") as f:
                f.write(cv)
            
            print(f"💾 Saved to: {cv_file}")
            
            # Show preview
            print("\n" + "=" * 80)
            print("CV PREVIEW (first 800 characters)")
            print("=" * 80)
            print(cv[:800])
            if len(cv) > 800:
                print("...")
            
            return cv
        else:
            print(f"❌ Failed to generate CV: {cv}")
            return None
    except Exception as e:
        print(f"❌ Error running tool: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_with_custom_job():
    """Test with a custom job offer"""
    print("\n\n" + "=" * 80)
    print("TEST 3: Testing with custom job offer")
    print("=" * 80)
    
    custom_job = """
Senior Data Scientist - Machine Learning

Company: AI Innovations Ltd

Position: Senior Data Scientist specializing in Machine Learning and AI

Requirements:
- 3+ years of experience in data science and machine learning
- Expert-level Python programming
- Deep understanding of ML algorithms and frameworks (TensorFlow, PyTorch, scikit-learn)
- Experience deploying production ML models
- Strong statistical analysis and modeling skills
- PhD or Master's degree in relevant field

Responsibilities:
- Lead ML projects from conception to deployment
- Build scalable ML pipelines
- Mentor junior data scientists
- Research and implement cutting-edge ML techniques
- Present findings to executive leadership

Location: Remote
"""
    
    custom_assessment = """
This is a stretch position for the candidate as it requires 3+ years and senior-level expertise.
The candidate has strong foundational skills but may need to emphasize learning ability and 
any advanced projects or research. The master's degree is a plus.
"""
    
    # Load profile
    print("\n📋 Loading user profile...")
    profile = load_profile()
    
    if not profile:
        print("❌ Failed to load profile!")
        return None
    
    print(f"✅ Profile loaded")
    
    # Generate CV
    print("\n⏳ Generating CV for custom job...")
    
    cv = generate_cv_sync(custom_job, profile, custom_assessment)
    
    if cv and not cv.startswith("Error"):
        print(f"✅ CV generated successfully ({len(cv)} characters)")
        
        # Save to file
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        cv_file = output_dir / "test_custom_job_cv.txt"
        with open(cv_file, "w", encoding="utf-8") as f:
            f.write(cv)
        
        print(f"💾 Saved to: {cv_file}")
        
        # Show preview
        print("\n" + "=" * 80)
        print("CV PREVIEW (first 600 characters)")
        print("=" * 80)
        print(cv[:600])
        if len(cv) > 600:
            print("...")
        
        return cv
    else:
        print(f"❌ Failed to generate CV: {cv}")
        return None


def compare_outputs():
    """Compare all generated CVs"""
    print("\n\n" + "=" * 80)
    print("OUTPUT COMPARISON")
    print("=" * 80)
    
    output_dir = Path(__file__).parent.parent / "output"
    cv_files = list(output_dir.glob("test_*.txt"))
    
    if not cv_files:
        print("⚠️ No output files found!")
        return
    
    print(f"\n📊 Found {len(cv_files)} CV files:\n")
    
    for cv_file in cv_files:
        with open(cv_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 {cv_file.name}")
        print(f"   Size: {len(content)} characters")
        print(f"   Lines: {len(content.splitlines())}")
        print(f"   Has 'PROFESSIONAL SUMMARY': {'Yes' if 'PROFESSIONAL SUMMARY' in content else 'No'}")
        print(f"   Has 'SKILLS': {'Yes' if 'SKILLS' in content else 'No'}")
        print(f"   Has 'EXPERIENCE': {'Yes' if 'EXPERIENCE' in content else 'No'}")
        print()


def main():
    """Run all tests"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "CV GENERATOR TOOL TEST SUITE" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")
    
    results = []
    
    # Test 1: Sync function
    result1 = test_sync_function()
    results.append(("Sync Function Test", result1 is not None))
    
    # Test 2: Tool class
    result2 = test_tool_class()
    results.append(("Tool Class Test", result2 is not None))
    
    # Test 3: Custom job
    result3 = test_with_custom_job()
    results.append(("Custom Job Test", result3 is not None))
    
    # Compare outputs
    compare_outputs()
    
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
    print("\n💡 To view a CV file:")
    print(f"   type {output_dir}\\test_sync_cv.txt")


if __name__ == "__main__":
    main()
