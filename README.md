# Job Seeking Automation with LangGraph & Gemini

An intelligent, agent-based job seeking automation system built with **LangGraph**, **LangChain**, and **Google's Gemini AI**. This system automates the entire job seeking workflow from profile creation to interview preparation using a sophisticated multi-agent architecture.

## 🌟 Features

- **🤖 Graph-Based Agent Architecture**: Built entirely on LangGraph for reliable, stateful agent orchestration
- **📄 Intelligent CV Parsing**: Extracts structured information from PDFs, DOCX, and text files
- **🔍 Smart Job Discovery**: Parses job descriptions from text or URLs
- **🎯 AI-Powered Matching**: Scores and ranks jobs based on profile fit (0-100 scale)
- **✍️ Tailored Applications**: Generates customized CVs and cover letters for each position
- **📊 Application Tracking**: Manages application status and provides follow-up recommendations
- **🎤 Interview Preparation**: Generates likely questions with STAR-format model answers

## 🏗️ Architecture

This project uses **LangGraph's StateGraph** to create a robust, graph-based workflow where each agent is a specialized node:

```
Profile Agent → Job Agent → Matching Agent → Application Agent → Tracking Agent
                                                                          ↓
                                                               Interview Agent
```

Each agent:
- Maintains its own state using TypedDict schemas
- Implements a LangGraph StateGraph
- Can be used independently or as part of the orchestrated workflow
- Handles errors gracefully with retry logic

## 📁 Project Structure

```
build_with_ai/
├── agents/                  # LangGraph-based agents
│   ├── base_agent.py       # Abstract base class
│   ├── state.py            # State schemas for all agents
│   ├── profile_agent.py    # CV parsing & profile building
│   ├── job_agent.py        # Job discovery & parsing
│   ├── matching_agent.py   # Job-profile matching
│   ├── application_agent.py # CV & cover letter generation
│   ├── tracking_agent.py   # Application tracking
│   └── interview_agent.py  # Interview preparation
├── config/
│   ├── settings.yaml       # Configuration
│   └── prompts.yaml        # AI prompts for each agent
├── context/                # Data storage (gitignored)
│   ├── user_profile.json
│   ├── job_listings.json
│   └── applications.json
├── tools/                  # Reusable utilities
│   ├── gemini_client.py    # Gemini API wrapper
│   ├── cv_parser.py        # CV parsing utilities
│   ├── web_scraper.py      # Job listing scraper
│   └── pdf_generator.py    # Document generation
├── scripts/
│   ├── init_project.py     # Project initialization
│   └── example_usage.py    # Usage examples
├── main.py                 # Main orchestrator
└── requirements.txt        # Dependencies
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd build_with_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google API key
# Get one from: https://makersuite.google.com/app/apikey
```

Edit `.env`:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Initialize Project

```bash
python scripts/init_project.py
```

### 4. Run Examples

```bash
# See example usage
python scripts/example_usage.py
```

## 💡 Usage Examples

### Example 1: Build Profile from CV

```python
from agents import ProfileAgent

agent = ProfileAgent()
profile = agent.run(
    cv_path="my_cv.pdf",
    user_preferences={
        "desired_roles": ["Software Engineer", "ML Engineer"],
        "location": "Remote",
        "min_salary": 120000
    }
)
```

### Example 2: Parse Job Listing

```python
from agents import JobAgent

agent = JobAgent()

# From text
job = agent.run(
    job_input="Senior Developer position at TechCorp...",
    job_source="text"
)

# From URL
job = agent.run(
    job_input="https://company.com/careers/123",
    job_source="url"
)
```

### Example 3: Match Jobs with Profile

```python
from agents import MatchingAgent

agent = MatchingAgent()

# Match all jobs in context/job_listings.json
matched_jobs = agent.run()

# Top matches with scores
for job in matched_jobs[:5]:
    print(f"{job['job_title']}: {job['match_score']}/100")
```

### Example 4: Generate Applications

```python
from agents import ApplicationAgent

agent = ApplicationAgent()

result = agent.run(
    job_posting=job_data,
    matching_analysis=match_analysis
)

print(f"CV: {result['cv_path']}")
print(f"Cover Letter: {result['cover_letter_path']}")
```

### Example 5: Full Automated Workflow

```python
from main import JobSeekingOrchestrator

orchestrator = JobSeekingOrchestrator()

result = orchestrator.run_full_workflow(
    cv_path="my_cv.pdf",
    job_inputs=[
        {"source": "text", "data": "Job description 1..."},
        {"source": "url", "data": "https://jobs.com/posting"}
    ],
    preferences={"desired_roles": ["Engineer"], "location": "Remote"},
    max_applications=3
)

# Result contains:
# - user_profile
# - job_listings  
# - matched_jobs
# - applications (with generated documents)
```

### Example 6: Interview Preparation

```python
orchestrator = JobSeekingOrchestrator()

result = orchestrator.prepare_interview(job_posting={
    "job_title": "Senior Engineer",
    "company_name": "TechCorp",
    "required_skills": ["Python", "AWS", "Leadership"]
})

# Get technical & behavioral questions with model answers
questions = result['questions']
```

## 🔧 Configuration

### Settings (`config/settings.yaml`)

```yaml
api:
  google_api_key: ${GOOGLE_API_KEY}
  model_name: "gemini-2.0-flash-exp"
  temperature: 0.7

agents:
  matching_agent:
    min_match_score: 60  # Minimum score to consider a match
  
  application_agent:
    enabled: true
```

### Prompts (`config/prompts.yaml`)

Centralized system prompts for each agent. Customize to adjust AI behavior:

```yaml
profile_agent:
  system_prompt: |
    You are an expert HR analyst...
  
matching_agent:
  system_prompt: |
    You are an expert career counselor...
```

## 🎯 LangGraph Implementation Details

### State Management

Each agent uses typed state schemas:

```python
from typing import TypedDict
from langgraph.graph import StateGraph

class ProfileState(TypedDict):
    cv_text: Optional[str]
    extracted_profile: Optional[Dict]
    status: str
    error: Optional[str]
```

### Graph Creation

Agents create graphs using StateGraph:

```python
def create_graph(self):
    builder = StateGraph(ProfileState)
    
    # Add nodes
    builder.add_node("parse_cv", self.parse_cv_node)
    builder.add_node("extract_profile", self.extract_profile_node)
    builder.add_node("save_profile", self.save_profile_node)
    
    # Define edges
    builder.add_edge(START, "parse_cv")
    builder.add_edge("parse_cv", "extract_profile")
    builder.add_edge("extract_profile", "save_profile")
    builder.add_edge("save_profile", END)
    
    return builder.compile()
```

### Orchestration

The main orchestrator coordinates all agents in a larger graph:

```python
builder = StateGraph(OrchestratorState)
builder.add_node("profile_building", self.profile_building_node)
builder.add_node("job_discovery", self.job_discovery_node)
builder.add_node("matching", self.matching_node)
# ... more nodes
```

## 📊 Output

Generated documents are saved in `context/generated_docs/`:

```
generated_docs/
├── TechCorp_Senior_Engineer_20240215_143022/
│   ├── cv.md
│   ├── cv.pdf
│   ├── cover_letter.md
│   └── cover_letter.pdf
```

## 🔐 Privacy & Security

- All personal data stays local in the `context/` directory
- `context/*.json` files are gitignored by default
- Never commit CVs or personal information
- API calls to Gemini are made securely via official SDK

## 🛠️ Development

### Adding a New Agent

1. Define state in `agents/state.py`
2. Create agent class extending `BaseAgent`
3. Implement `create_graph()` method
4. Add node functions for each step
5. Register in `agents/__init__.py`

### Testing Individual Agents

```python
# Test a single agent
from agents import ProfileAgent

agent = ProfileAgent()
graph = agent.create_graph()

# Invoke with test state
result = graph.invoke({
    "cv_text": "test CV content",
    "status": "initialized"
})
```

## 📚 Dependencies

- **langchain** - LangChain framework
- **langgraph** - Graph-based agent orchestration
- **langchain-google-genai** - Gemini integration
- **google-generativeai** - Google AI SDK
- **pydantic** - Data validation
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing
- **beautifulsoup4** - Web scraping
- **reportlab** - PDF generation

## 🤝 Contributing

1. Follow the LangGraph patterns in existing agents
2. Use typed state schemas
3. Add error handling to all nodes
4. Update documentation

## 📖 Documentation

- [Implementation Guide](docs/implementation_guide.md) - Detailed implementation steps
- [System Architecture](docs/system_architecture.md) - Architecture overview
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/) - Official LangGraph documentation

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- [Google Gemini](https://deepmind.google/technologies/gemini/) by Google DeepMind

---

**Made with ❤️ using LangGraph and Gemini AI**
