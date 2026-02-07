"""
Test script for PDF Converter Tool
Tests conversion of CV and cover letter from txt to PDF
"""
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from tools.pdf_converter import convert_txt_to_pdf, convert_application_materials_to_pdf


def test_manual_pdf_conversion():
    """Test converting a specific job folder's materials to PDF"""
    print("🧪 PDF Converter Test\n")
    print("="*60)
    
    # Find the most recent job folder
    output_dir = parent_dir / "output"
    job_folders = [f for f in output_dir.iterdir() if f.is_dir() and not f.name.startswith('.')]
    
    if not job_folders:
        print("❌ No job folders found in output directory")
        return
    
    # Sort by modification time, get most recent
    most_recent_folder = max(job_folders, key=lambda f: f.stat().st_mtime)
    
    print(f"📁 Testing with folder: {most_recent_folder.name}\n")
    
    # Check if txt files exist
    cv_txt = most_recent_folder / "cv.txt"
    cover_txt = most_recent_folder / "cover_letter.txt"
    
    if not cv_txt.exists():
        print("❌ cv.txt not found in folder")
        return
    
    if not cover_txt.exists():
        print("❌ cover_letter.txt not found in folder")
        return
    
    print("✓ Found cv.txt")
    print("✓ Found cover_letter.txt\n")
    
    print("-"*60)
    print("Converting to PDF...\n")
    
    # Test individual conversions
    print("1️⃣  Converting CV...")
    cv_pdf = most_recent_folder / "cv.pdf"
    result_cv = convert_txt_to_pdf(
        str(cv_txt),
        str(cv_pdf),
        document_type="cv"
    )
    print(f"   {result_cv}\n")
    
    print("2️⃣  Converting Cover Letter...")
    cover_pdf = most_recent_folder / "cover_letter.pdf"
    result_cover = convert_txt_to_pdf(
        str(cover_txt),
        str(cover_pdf),
        document_type="cover_letter"
    )
    print(f"   {result_cover}\n")
    
    print("-"*60)
    print("\n📊 Verification:")
    print(f"   CV PDF exists: {'✓' if cv_pdf.exists() else '✗'}")
    print(f"   Cover PDF exists: {'✓' if cover_pdf.exists() else '✗'}")
    
    if cv_pdf.exists():
        print(f"   CV PDF size: {cv_pdf.stat().st_size / 1024:.1f} KB")
    if cover_pdf.exists():
        print(f"   Cover PDF size: {cover_pdf.stat().st_size / 1024:.1f} KB")
    
    print(f"\n📂 All files in folder:")
    for file in sorted(most_recent_folder.iterdir()):
        if file.is_file():
            size_kb = file.stat().st_size / 1024
            print(f"   • {file.name} ({size_kb:.1f} KB)")


def test_batch_conversion():
    """Test the convenience function that converts both files at once"""
    print("\n" + "="*60)
    print("🧪 Testing Batch Conversion\n")
    
    output_dir = parent_dir / "output"
    job_folders = [f for f in output_dir.iterdir() if f.is_dir() and not f.name.startswith('.')]
    
    if not job_folders:
        print("❌ No job folders found")
        return
    
    most_recent_folder = max(job_folders, key=lambda f: f.stat().st_mtime)
    
    print(f"📁 Converting all materials in: {most_recent_folder.name}\n")
    
    results = convert_application_materials_to_pdf(str(most_recent_folder))
    
    print("Results:")
    print(f"   CV: {results['cv']}")
    print(f"   Cover Letter: {results['cover_letter']}")


if __name__ == "__main__":
    print("🚀 PDF CONVERTER TEST SUITE")
    print("="*60 + "\n")
    
    try:
        # Test 1: Manual conversion
        test_manual_pdf_conversion()
        
        # Test 2: Batch conversion
        # test_batch_conversion()  # Uncomment if you want to test batch conversion
        
        print("\n" + "="*60)
        print("✅ PDF CONVERTER TEST COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
