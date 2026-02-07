"""
Simple test script for cv_generator.py
Quick test with minimal setup - No async required
"""

import yaml
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.cv_generator import generate_cv_sync


def load_profile():
    """Load profile from YAML"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data, default_flow_style=False, allow_unicode=True)


def quick_test():
    """Quick test of CV generation - Synchronous only"""
    
    print("🚀 Quick CV Generator Test (Synchronous)\n")
    
    # Simple job offer
    job_offer = """
Data Scientist Position
Requirements: Python, SQL, Machine Learning, 2+ years experience
Responsibilities: Build models, analyze data, create dashboards
"""
    
    # Simple assessment
    assessment = "Good match. Candidate has relevant skills and experience."
    
    # Load profile
    print("📋 Loading profile...")
    profile = load_profile()
    print(f"✅ Profile loaded ({len(profile)} chars)\n")
    
    # Generate CV (synchronous)
    print("⏳ Generating CV...")
    cv = generate_cv_sync(job_offer, profile, assessment)
    
    # Display result
    if cv and not cv.startswith("Error"):
        print(f"✅ CV Generated!\n")
        print("=" * 60)
        print(cv)
        print("=" * 60)
        
        # Save to central output folder
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "quick_test_cv.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cv)
        
        print(f"\n💾 Saved to: {output_file}")
        print(f"📏 Length: {len(cv)} characters")
    else:
        print(f"❌ Error: {cv}")


if __name__ == "__main__":
    quick_test()
