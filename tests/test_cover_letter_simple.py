"""
Simple test script for cover_letter_generator.py
Quick test with minimal setup
"""

import yaml
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.cover_letter_generator import generate_cover_letter_sync
from tools.job_assessment_tool import assess_job_match


def load_profile() -> str:
    """Load profile from YAML"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


def quick_test():
    """Quick test of cover letter generation"""
    
    print("🚀 Quick Cover Letter Generator Test\n")
    
    # Simple job offer
    job_offer = """
Data Scientist Position

Company: TechCorp Tunisia
Location: Tunis, Tunisia

Requirements:
- 2+ years experience in data science
- Python (pandas, scikit-learn)
- SQL and data analysis
- Machine learning knowledge
- Master's degree in Data Science

Responsibilities:
- Build predictive models
- Analyze data and create insights
- Work with cross-functional teams

To Apply: Send CV and cover letter to jobs@techcorp.tn
"""
    
    # Load profile
    print("📋 Loading profile...")
    profile = load_profile()
    print(f"✅ Profile loaded\n")
    
    # Get job assessment first
    print("📊 Assessing job match...")
    assessment = assess_job_match(job_offer, profile)
    
    try:
        assessment_data = json.loads(assessment)
        match_score = assessment_data.get('match_score', 0)
        print(f"✅ Match Score: {match_score}/100\n")
    except:
        print("✅ Assessment complete\n")
    
    # Generate cover letter
    print("📝 Generating cover letter...")
    cover_letter = generate_cover_letter_sync(job_offer, profile, assessment)
    
    # Display result
    if cover_letter and not cover_letter.startswith("Error"):
        print("✅ Cover Letter Generated!\n")
        print("=" * 70)
        print(cover_letter)
        print("=" * 70)
        
        # Save to central output folder
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "quick_test_cover_letter.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        # Stats
        word_count = len(cover_letter.split())
        line_count = len(cover_letter.splitlines())
        
        print(f"\n📊 Statistics:")
        print(f"   💾 Saved to: {output_file}")
        print(f"   📏 Words: {word_count}")
        print(f"   📄 Lines: {line_count}")
        print(f"   📝 Characters: {len(cover_letter)}")
        
        # Quality checks
        has_contact = "@" in cover_letter
        has_position = "Data Scientist" in cover_letter
        has_company = "TechCorp" in cover_letter or "company" in cover_letter.lower()
        has_closing = "Sincerely" in cover_letter or "regards" in cover_letter.lower()
        
        print(f"\n✓ Quality Checks:")
        print(f"   Contact Info: {'✓' if has_contact else '✗'}")
        print(f"   Position Mentioned: {'✓' if has_position else '✗'}")
        print(f"   Company Referenced: {'✓' if has_company else '✗'}")
        print(f"   Professional Closing: {'✓' if has_closing else '✗'}")
        
        # Recommendation
        if 250 <= word_count <= 450:
            print(f"\n🎯 Length: Perfect (250-450 words)")
        elif word_count < 250:
            print(f"\n⚠️  Length: A bit short (aim for 300-400 words)")
        else:
            print(f"\n⚠️  Length: A bit long (aim for 300-400 words)")
        
    else:
        print(f"❌ Error: {cover_letter}")


if __name__ == "__main__":
    quick_test()
