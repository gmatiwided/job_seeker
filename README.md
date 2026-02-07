# 🎯 AI-Powered Job Application Assistant

A comprehensive, intelligent system built with **LangGraph** and **Google Gemini** that automates the entire job application process—from evaluating job fit to generating professional application materials.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-green.svg)](https://www.langchain.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)](https://ai.google.dev/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Core Components](#-core-components)
- [Usage Guide](#-usage-guide)
- [Testing](#-testing)
- [Output Structure](#-output-structure)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)

---

## 🚀 Features

### **Intelligent Job Assessment**
- ✅ Evaluates job match based on candidate profile
- ✅ Provides detailed scoring (0-100) with weighted criteria
- ✅ Identifies strengths and gaps
- ✅ Offers actionable recommendations

### **Automated Document Generation**
- ✅ **ATS-Friendly CVs** - Plain text, optimized for Applicant Tracking Systems
- ✅ **Professional Cover Letters** - Tailored to each job posting
- ✅ **Interview Preparation Guides** - Technical & behavioral questions with model answers
- ✅ **PDF Conversion** - Automatic conversion of text documents to formatted PDFs

### **Smart Workflow Management**
- ✅ LangGraph-based state machine with tool orchestration
- ✅ Sequential execution (Assess → CV → Cover → Interview → PDF)
- ✅ Duplicate prevention and safety limits
- ✅ Automatic file organization in job-specific folders

### **Quality & Authenticity**
- ✅ No hallucination - All content based strictly on provided profile
- ✅ Honest assessment - Doesn't generate materials for poor matches (<60%)
- ✅ Constructive feedback - Highlights areas for improvement
- ✅ Professional formatting - Clean, readable documents

---

## 📁 Project Structure

```
build_with_ai/
├── agents/                      # LangGraph agents
│   ├── job_seeker.py           # Main job application agent
│   ├── cv_generator_agent.py   # Standalone CV generator agent
│   ├── BUGFIXES.md             # Bug fix documentation
│   └── PDF_FIX.md              # PDF conversion solution
│
├── tools/                       # LangChain tools
│   ├── __init__.py             # Tool exports
│   ├── cv_generator.py         # CV generation tool
│   ├── job_assessment_tool.py  # Job matching assessment
│   ├── cover_letter_generator.py # Cover letter generation
│   ├── interview_prep_generator.py # Interview prep guide
│   └── pdf_converter.py        # Text to PDF conversion
│
├── tests/                       # Test scripts
│   ├── test_job_seeker_simple.py      # Quick agent test
│   ├── test_job_seeker_agent.py       # Full agent test suite
│   ├── test_cv_generator.py           # CV generator tests
│   ├── test_cv_generator_simple.py    # Quick CV test
│   ├── test_job_assessment.py         # Assessment tests
│   ├── test_cover_letter.py           # Cover letter tests
│   ├── test_interview_prep.py         # Interview prep tests
│   └── check_pdf_capability.py        # PDF diagnostic tool
│
├── config/                      # Configuration files
│   └── profile.yaml            # Candidate profile data
│
├── output/                      # Generated materials
│   └── [Job-specific folders]/
│       ├── job_offer.txt       # Original job posting
│       ├── assessment.json     # Match analysis
│       ├── cv.txt              # Generated CV (text)
│       ├── cv.pdf              # Generated CV (PDF)
│       ├── cover_letter.txt    # Cover letter (text)
│       ├── cover_letter.pdf    # Cover letter (PDF)
│       └── interview_prep.md   # Interview guide
│
└── scripts/                     # Utility scripts
    ├── initial_script.py       # Basic Gemini setup
    └── initiation_langgraph.ipynb # LangGraph tutorial
```

---

## 🔧 Installation

### **Prerequisites**
- Python 3.8 or higher
- Google API key (for Gemini access)
- Virtual environment (recommended)

### **Step 1: Clone Repository**
```bash
git clone <repository-url>
cd build_with_ai
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install langchain langchain-google-genai langgraph reportlab pyyaml
```

Or use requirements file (if available):
```bash
pip install -r requirements.txt
```

### **Step 4: Configure API Key**

**Option A: Environment Variable**
```bash
# Windows
set GOOGLE_API_KEY=your_api_key_here

# macOS/Linux
export GOOGLE_API_KEY=your_api_key_here
```

**Option B: Direct Configuration**
Edit the API key in the tool files (not recommended for production):
```python
api_key = "your_api_key_here"
```

---

## 🚀 Quick Start

### **1. Configure Your Profile**

Edit `config/profile.yaml` with your information:

```yaml
name: Your Name
headline: "Job Title | Skills | Value Proposition"
location: Your Location
email: your.email@example.com
phone: +1234567890
linkedin: https://linkedin.com/in/yourprofile
github: https://github.com/yourusername

professional_overview: >
  Your professional summary here...

skills:
  technical:
    - Python
    - SQL
    - Machine Learning
  soft_skills:
    - Communication
    - Problem-solving

experience:
  - role: "Your Job Title"
    company: "Company Name"
    duration: "2 years"
    location: "City, Country"
    achievements:
      - "Quantified achievement 1"
      - "Quantified achievement 2"

education:
  - degree: "Your Degree"
    field: "Field of Study"
    institution: "University Name"
    year: 2020

# ... more fields
```

### **2. Run Your First Job Application**

```python
from agents.job_seeker import process_job_application

job_offer = """
Data Scientist
TechCorp Inc.

Requirements:
- 2+ years experience in Python
- Strong SQL and ML skills
- Experience with data visualization

Responsibilities:
- Build predictive models
- Create dashboards
- Collaborate with teams
"""

result = process_job_application(
    job_offer=job_offer,
    job_title="Data Scientist",
    company="TechCorp"
)

print(f"All files saved in: {result['job_folder']}")
```

### **3. Check Your Output**

Navigate to `output/TechCorp_DataScientist_YYYYMMDD_HHMMSS/` to find:
- ✅ assessment.json (match analysis)
- ✅ cv.txt & cv.pdf (your tailored CV)
- ✅ cover_letter.txt & cover_letter.pdf
- ✅ interview_prep.md (interview guide)

---

## ⚙️ Configuration

### **Profile Configuration** (`config/profile.yaml`)

The profile contains all your professional information:

```yaml
# Personal Information
name: Full Name
headline: Professional headline
location: City, Country
email: email@example.com
phone: Phone number
linkedin: LinkedIn URL
github: GitHub URL (optional)

# Professional Overview
professional_overview: >
  2-3 paragraph summary of your professional background

# Skills
skills:
  technical:
    - Skill 1
    - Skill 2
  tools:
    - Tool 1
    - Tool 2
  soft_skills:
    - Soft skill 1

# Experience
experience:
  - role: Job Title
    company: Company Name
    duration: Time period
    location: Location
    achievements:
      - Achievement 1 (with metrics)
      - Achievement 2

# Projects (optional)
projects:
  - name: Project Name
    description: What you built
    technologies:
      - Tech 1
      - Tech 2

# Education
education:
  - degree: Degree name
    field: Field of study
    institution: School name
    year: Graduation year
    gpa: GPA (optional)

# Certifications (optional)
certifications:
  - name: Certification name
    issuer: Issuing organization
    year: Year obtained

# Languages (optional)
languages:
  - language: Language name
    proficiency: Level (Native, Fluent, etc.)
```

### **Tool Configuration**

Each tool can be configured by modifying its source file:

**Model Settings** (in each tool):
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Model version
    temperature=0.7,            # Creativity (0-1)
    max_retries=2,              # Retry on failure
    google_api_key=api_key,
)
```

**Output Token Limits**:
- CV Generator: 2000 tokens
- Cover Letter: 1500 tokens
- Interview Prep: 9000 tokens
- Job Assessment: 2000 tokens

---

## 🛠️ Core Components

### **1. Job Seeker Agent** (`agents/job_seeker.py`)

The main orchestrator that manages the entire application workflow.

**Features:**
- State-based workflow management
- Sequential tool execution
- Automatic PDF generation
- Job-specific folder organization
- Duplicate prevention
- Safety limits (max 8 tool calls)

**Workflow:**
```
1. Assess Job Match (JobAssessmentTool)
   ↓
2. Check Score
   ├─ ≥60%: Continue
   └─ <60%: Stop with feedback
   ↓
3. Generate CV (CVGeneratorTool)
   ↓
4. Generate Cover Letter (CoverLetterGeneratorTool)
   ↓
5. Generate Interview Prep (InterviewPrepTool)
   ↓
6. Save all files & Convert to PDF
```

### **2. Tools**

#### **Job Assessment Tool** (`tools/job_assessment_tool.py`)
- Evaluates candidate-job fit
- Weighted scoring system (Skills, Experience, Domain, Education, Culture)
- Provides match score (0-100), strengths, gaps, recommendations
- Output: JSON format

#### **CV Generator** (`tools/cv_generator.py`)
- Creates ATS-friendly CVs
- Plain text format (no special characters)
- Fact-based (no hallucinations)
- Tailored to job description
- Output: TXT format

#### **Cover Letter Generator** (`tools/cover_letter_generator.py`)
- Professional business letter format
- Uses job assessment insights
- Addresses gaps constructively
- 300-400 words target length
- Output: TXT format

#### **Interview Prep Generator** (`tools/interview_prep_generator.py`)
- 8-10 questions (5-6 technical, 2-3 behavioral, 1-2 fit)
- Model answers (60-100 words each)
- STAR format for behavioral questions
- Concise and practical
- Output: Markdown format

#### **PDF Converter** (`tools/pdf_converter.py`)
- Converts TXT to professional PDF
- Smart formatting (detects headers, contact info)
- ATS-compatible layout
- Uses ReportLab library
- Output: PDF format

### **3. Agent State Management**

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int
    tools_called: list      # Track executed tools
    job_folder: str         # Job-specific output folder
```

---

## 📖 Usage Guide

### **Scenario 1: Quick Single Job Application**

```bash
python tests/test_job_seeker_simple.py
```

Modify the job description in the test file for your needs.

### **Scenario 2: Programmatic Usage**

```python
from agents.job_seeker import process_job_application

# Your job posting
job_description = """..."""

# Process application
result = process_job_application(
    job_offer=job_description,
    job_title="Software Engineer",
    company="Google"
)

# Access results
print(f"Match Score: {result['assessment']}")
print(f"CV Generated: {result['cv'] is not None}")
print(f"PDF Created: {result['cv_pdf']}")
print(f"Folder: {result['job_folder']}")
```

### **Scenario 3: Testing Individual Tools**

**Test CV Generator:**
```bash
python tests/test_cv_generator_simple.py
```

**Test Job Assessment:**
```bash
python tests/test_job_assessment_simple.py
```

**Test Cover Letter:**
```bash
python tests/test_cover_letter_simple.py
```

**Test Interview Prep:**
```bash
python tests/test_interview_prep_simple.py
```

**Test PDF Conversion:**
```bash
python tests/check_pdf_capability.py
```

### **Scenario 4: Batch Processing Multiple Jobs**

```python
from agents.job_seeker import process_job_application

jobs = [
    {"title": "Data Scientist", "company": "TechCorp", "description": "..."},
    {"title": "ML Engineer", "company": "AI Inc", "description": "..."},
    {"title": "Analyst", "company": "DataCo", "description": "..."},
]

for job in jobs:
    try:
        result = process_job_application(
            job_offer=job['description'],
            job_title=job['title'],
            company=job['company']
        )
        print(f"✅ {job['company']} - {job['title']}: Generated!")
    except Exception as e:
        print(f"❌ {job['company']} - {job['title']}: {e}")
```

---

## 🧪 Testing

### **Test Suite Overview**

| Test File | Purpose | Duration |
|-----------|---------|----------|
| `test_job_seeker_simple.py` | Quick agent test (1 job) | ~60s |
| `test_job_seeker_agent.py` | Full test (good + poor match) | ~120s |
| `test_cv_generator.py` | CV generation (multiple scenarios) | ~40s |
| `test_job_assessment.py` | Assessment scoring | ~30s |
| `test_cover_letter.py` | Cover letter generation | ~30s |
| `test_interview_prep.py` | Interview prep creation | ~50s |
| `check_pdf_capability.py` | PDF conversion diagnostic | ~5s |

### **Running Tests**

**Run All Tests:**
```bash
# From project root
python tests/test_job_seeker_agent.py
python tests/test_cv_generator.py
python tests/test_job_assessment.py
python tests/test_cover_letter.py
python tests/test_interview_prep.py
```

**Run Quick Tests:**
```bash
python tests/test_job_seeker_simple.py
python tests/test_cv_generator_simple.py
```

**Check PDF Capability:**
```bash
python tests/check_pdf_capability.py
```

### **Expected Test Results**

✅ **Successful Test Output:**
```
🚀 Quick Job Seeker Agent Test
======================================================================
🎯 JOB SEEKER AGENT - Starting Application Process
======================================================================

📁 Job folder created: DataCo_Junior_Data_Scientist_20260207_143052
  ✓ Job offer saved

🤖 Agent processing job application...

🔧 Calling tool: assess_job_match
✅ Tool assess_job_match completed

🔧 Calling tool: generate_cv
✅ Tool generate_cv completed

🔧 Calling tool: generate_cover_letter
✅ Tool generate_cover_letter completed

🔧 Calling tool: generate_interview_prep
✅ Tool generate_interview_prep completed

✅ All materials generated, workflow complete!

💾 Saving materials to: ...
  ✓ Assessment saved
  ✓ CV saved (txt)
  ✓ Cover letter saved (txt)
  ✓ Interview prep saved

📄 Converting to PDF...
  ✅ PDF created successfully: cv.pdf (42.3 KB)
  ✅ PDF created successfully: cover_letter.pdf (28.5 KB)

📄 Files created:
   📊 assessment.json (2.5 KB)
   📋 cover_letter.txt (1.8 KB)
   📄 cover_letter.pdf (28.5 KB)
   📋 cv.txt (2.8 KB)
   📄 cv.pdf (42.3 KB)
   📝 interview_prep.md (8.2 KB)
   📋 job_offer.txt (0.4 KB)

✅ Test completed successfully!
```

---

## 📂 Output Structure

Each job application creates a unique folder with all materials:

```
output/
└── CompanyName_JobTitle_20260207_143052/
    ├── job_offer.txt          (400 bytes)   - Original job posting
    ├── assessment.json        (2.5 KB)      - Match analysis & score
    ├── cv.txt                 (2.8 KB)      - Generated CV (text)
    ├── cv.pdf                 (42.3 KB)     - Generated CV (PDF)
    ├── cover_letter.txt       (1.8 KB)      - Cover letter (text)
    ├── cover_letter.pdf       (28.5 KB)     - Cover letter (PDF)
    └── interview_prep.md      (8.2 KB)      - Interview preparation guide
```

### **File Descriptions**

| File | Format | Purpose |
|------|--------|---------|
| `job_offer.txt` | Plain text | Original job posting for reference |
| `assessment.json` | JSON | Match score, strengths, gaps, recommendations |
| `cv.txt` | Plain text | Editable CV version (ATS-friendly) |
| `cv.pdf` | PDF | Professional CV for submission |
| `cover_letter.txt` | Plain text | Editable cover letter version |
| `cover_letter.pdf` | PDF | Professional cover letter for submission |
| `interview_prep.md` | Markdown | Interview questions & answers |

---

## 🔬 Technical Details

### **Tech Stack**

- **Framework:** LangGraph (state-based agent orchestration)
- **LLM:** Google Gemini 2.5 Flash
- **LangChain:** Tool management and integration
- **ReportLab:** PDF generation
- **PyYAML:** Configuration management
- **Pydantic:** Data validation

### **LLM Configuration**

```python
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,           # Balance creativity/consistency
    max_retries=2,             # Retry on API errors
    google_api_key=api_key,
)
```

### **Agent Architecture**

The system uses a **state machine** pattern with LangGraph:

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LLM Node   │ ← System Instruction + Human Message
└──────┬──────┘
       │
       ▼
  Has tool calls?
       │
   ┌───┴───┐
   YES     NO → END
   │
   ▼
┌─────────────┐
│ Tools Node  │ ← Execute: assess, cv, cover, interview
└──────┬──────┘
       │
       └──→ Back to LLM
```

### **State Tracking**

```python
state = {
    "messages": [SystemMessage, HumanMessage, ToolMessage, ...],
    "number_of_steps": int,
    "tools_called": ["assess_job_match", "generate_cv", ...],
    "job_folder": "path/to/output/folder"
}
```

### **Tool Execution Flow**

1. **Tool Call Detection:** Check last message for tool_calls
2. **Duplicate Prevention:** Skip if tool already called
3. **Tool Invocation:** Execute tool with provided arguments
4. **Result Capture:** Store as ToolMessage
5. **State Update:** Add to tools_called list
6. **Completion Check:** Stop when all required tools executed

### **PDF Generation**

Uses ReportLab with custom formatting:
- **Page Size:** US Letter (8.5" x 11")
- **Margins:** 0.75 inches all sides
- **Fonts:** Helvetica (ATS-compatible)
- **Name:** 16pt, bold, centered
- **Contact:** 9pt, centered
- **Headers:** 14pt, bold
- **Body:** 10pt, regular

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. API Key Error**
```
Error: GOOGLE_API_KEY not found
```
**Solution:** Set your API key in environment variables or configure directly in code.

#### **2. Module Not Found**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution:** Install dependencies:
```bash
pip install langchain langchain-google-genai langgraph reportlab pyyaml
```

#### **3. PDF Not Created**
```
⚠️  CV PDF conversion called but file not found
```
**Solution:** Install ReportLab:
```bash
pip install reportlab
```

Run diagnostic:
```bash
python tests/check_pdf_capability.py
```

#### **4. Empty CV/Assessment Output**
**Cause:** Profile data missing or incomplete
**Solution:** Check `config/profile.yaml` has all required fields

#### **5. 500 Internal Server Error**
```
google.genai.errors.ServerError: 500 INTERNAL
```
**Cause:** Google API rate limiting or temporary issue
**Solution:** Wait a few seconds and retry

#### **6. Agent Calls Same Tool Multiple Times**
**Cause:** Old version before bugfix
**Solution:** Make sure you have the latest version with `tools_called` tracking

#### **7. Interview Prep Too Long/Incomplete**
**Cause:** Token limit reached
**Solution:** Already optimized to 9000 tokens with focused output

### **Debug Mode**

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📚 API Reference

### **Main Function**

#### `process_job_application(job_offer, job_title, company)`

**Parameters:**
- `job_offer` (str): Full job description text
- `job_title` (str, optional): Job title for folder naming
- `company` (str, optional): Company name for folder naming

**Returns:** dict
```python
{
    "assessment": str,           # JSON string with match analysis
    "cv": str,                   # CV text content
    "cover_letter": str,         # Cover letter text
    "interview_prep": str,       # Interview prep markdown
    "cv_pdf": bool,              # True if CV PDF created
    "cover_letter_pdf": bool,    # True if cover PDF created
    "job_folder": str,           # Path to output folder
    "folder_name": str           # Folder name
}
```

### **Individual Tools**

#### `generate_cv_sync(profile_details, job_description)`
Generates ATS-friendly CV.

#### `assess_job_match(profile_details, job_description)`
Evaluates job-candidate fit.

#### `generate_cover_letter_sync(profile_details, job_description, cv_content, job_assessment)`
Creates professional cover letter.

#### `generate_interview_prep_sync(job_offer, cv_content, cover_letter, job_assessment)`
Generates interview preparation guide.

#### `convert_txt_to_pdf(txt_file_path, output_pdf_path, document_type)`
Converts text file to formatted PDF.

---

## 🎯 Best Practices

### **Profile Management**
- ✅ Keep `profile.yaml` up to date
- ✅ Use quantified achievements (numbers, percentages)
- ✅ Be honest - no exaggerations
- ✅ Include relevant keywords for your field

### **Job Applications**
- ✅ Review assessment before applying
- ✅ Read generated materials before submission
- ✅ Customize if needed (edit txt files before PDF conversion)
- ✅ Focus on jobs with >70% match score

### **Output Management**
- ✅ Organize by company/date
- ✅ Keep both txt and PDF versions
- ✅ Archive old applications
- ✅ Track which jobs you've applied to

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional LLM model support (OpenAI, Anthropic)
- [ ] Web interface (Streamlit/Gradio)
- [ ] Email integration (auto-send applications)
- [ ] Job board scraping
- [ ] Resume parsing (import existing CVs)
- [ ] Multi-language support
- [ ] Custom templates
- [ ] Analytics dashboard

---

## 📄 License

This project is provided as-is for educational and personal use.

---

## 🙏 Acknowledgments

- **LangChain** - Framework for LLM applications
- **LangGraph** - State machine and agent orchestration
- **Google Gemini** - Powerful language model
- **ReportLab** - PDF generation library

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review test files for examples
3. Check documentation in individual tool files
4. Open an issue on the repository

---

## 🎓 Learn More

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

**Built with ❤️ using LangGraph and Google Gemini**

*Last Updated: February 2026*
