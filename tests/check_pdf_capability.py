"""
Quick check: Test if reportlab is installed and PDF generation works
"""
import sys
from pathlib import Path

print("🔍 Checking PDF conversion capabilities...\n")

# Check if reportlab is installed
try:
    import reportlab
    print("✅ reportlab is installed")
    print(f"   Version: {reportlab.Version}")
except ImportError:
    print("❌ reportlab is NOT installed")
    print("\n📦 Install with: pip install reportlab")
    sys.exit(1)

# Add parent to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Test PDF converter import
try:
    from tools.pdf_converter import convert_txt_to_pdf
    print("✅ PDF converter tool imported successfully\n")
except ImportError as e:
    print(f"❌ Failed to import PDF converter: {e}")
    sys.exit(1)

# Find a test file
output_dir = parent_dir / "output"
test_folders = [f for f in output_dir.iterdir() if f.is_dir() and not f.name.startswith('.')]

if not test_folders:
    print("⚠️  No job folders found to test")
    print("   Run test_job_seeker_simple.py first to generate test data")
    sys.exit(0)

# Get most recent folder
test_folder = max(test_folders, key=lambda f: f.stat().st_mtime)
print(f"📁 Testing with folder: {test_folder.name}\n")

# Check for txt files
cv_txt = test_folder / "cv.txt"
cover_txt = test_folder / "cover_letter.txt"

if not cv_txt.exists():
    print(f"❌ cv.txt not found in {test_folder.name}")
    sys.exit(1)

print(f"✅ Found cv.txt ({cv_txt.stat().st_size / 1024:.1f} KB)")

# Test PDF conversion
print("\n" + "="*60)
print("🔄 Testing PDF Conversion...")
print("="*60 + "\n")

cv_pdf = test_folder / "cv_test.pdf"
result = convert_txt_to_pdf(
    str(cv_txt),
    str(cv_pdf),
    document_type="cv"
)

print(f"Result: {result}")

if cv_pdf.exists():
    print(f"\n✅ PDF CREATED SUCCESSFULLY!")
    print(f"   Location: {cv_pdf}")
    print(f"   Size: {cv_pdf.stat().st_size / 1024:.1f} KB")
else:
    print(f"\n❌ PDF was not created")
    print(f"   Expected at: {cv_pdf}")

print("\n" + "="*60)
print("✅ PDF Conversion Test Complete")
print("="*60)
