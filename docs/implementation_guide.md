 # Build with AI: Job Seeking with Gemini - Implementation Guide

## 1. Project Overview
This project automates the job-seeking process using Google's Gemini models. It employs an agentic architecture to handle specific stages of the pipeline: Profile Building, Job Discovery, Matching, Application Generation, Tracking, and Interview Preparation.

## 2. Directory Structure & Architecture
The project follows a modular, agent-based structure designed for scalability and maintainability.

```text
build_with_ai/
├── agents/             # Core logic for specific tasks
│   ├── base_agent.py   # Abstract base class for all agents
│   ├── profile_agent.py
│   ├── job_agent.py
│   ├── matching_agent.py
│   ├── application_agent.py
│   ├── tracking_agent.py
│   └── interview_agent.py
├── config/             # Configuration settings
│   ├── settings.yaml   # API keys, global settings (model versions)
│   └── prompts.yaml    # Centralized System Prompts for Gemini
├── context/            # Data storage (JSON/Markdown) acting as memory
│   ├── user_profile.json
│   ├── job_listings.json
│   ├── applications.json
│   └── project_overview.md
├── docs/               # Project documentation
│   ├── system_architecture.mmd
│   └── implementation_guide.md
├── scripts/            # Utility scripts for setup and maintenance
│   └── init_db.py
├── tools/              # Reusable tools for Agents
│   ├── cv_parser.py
│   ├── web_scraper.py
│   ├── pdf_generator.py
│   └── gemini_client.py
└── main.py             # Entry point / Orchestrator
```

## 3. Implementation Flow & Step-by-Step Guide

### Phase 1: Foundation & Profile Agent
**Goal:** Create a robust "Context" layer that understands the user.

1.  **Environment Setup**:
    *   Set up Python virtual environment.
    *   Install dependencies: `google-generativeai`, `langchain` (optional but recommended), `pydantic`.
    *   Configure `config/settings.yaml` for Gemini API keys.
2.  **Tool Implementation (`tools/`)**:
    *   `gemini_client.py`: Wrapper for Gemini API calls with error handling and retries.
    *   `cv_parser.py`: Uses libraries like `PyPDF2` or `python-docx` to extract raw text, then passes it to Gemini to structure into JSON.
3.  **Profile Agent (`agents/profile_agent.py`)**:
    *   **Input**: Raw CV text, User preferences.
    *   **Process**: Prompt Gemini to extract: Skills, Experience, Education, Preferred Roles.
    *   **Output**: Save to `context/user_profile.json`.

### Phase 2: Job Discovery & Matching
**Goal:** Find jobs and score them against the profile.

1.  **Job Agent (`agents/job_agent.py`)**:
    *   **Manual Mode**: Accepts text/URL, scrapes content using `tools/web_scraper.py`, and structures it.
    *   **Auto Mode** (Advanced): Connects to job board APIs or uses search tools.
    *   **Output**: standardized job objects in `context/job_listings.json`.
2.  **Matching Agent (`agents/matching_agent.py`)**:
    *   **Logic**: Retrieves `user_profile` and `job_listings`.
    *   **Scoring**: Asks Gemini to rate the fit (0-100) and provide a "Gap Analysis" (missing skills).
    *   **Output**: Updates `job_listings.json` with scores.

### Phase 3: Application Factory
**Goal:** Generate hyper-personalized documents.

1.  **Application Agent (`agents/application_agent.py`)**:
    *   **Context**: Takes the top-matched job and the user profile.
    *   **Prompting Strategy**: "Act as an expert copywriter. Rewrite this CV bullet point to match this Job Requirement..."
    *   **Output**: Markdown strings for CV and Cover Letter.
2.  **PDF Generation (`tools/pdf_generator.py`)**:
    *   Convert the Markdown output into a professional PDF/DOCX format.

### Phase 4: Tracking & Interview Coach
**Goal:** Manage lifecycle and prepare for success.

1.  **Tracking Agent (`agents/tracking_agent.py`)**:
    *   Simple state machine: Applied -> Interviewing -> Offer.
    *   Stores dates and status in `context/applications.json`.
2.  **Interview Agent (`agents/interview_agent.py`)**:
    *   **Input**: Job Description + Application Documents.
    *   **Action**: Generate 5 technical and 5 behavioral questions.
    *   **Simulation**: Interactive chat loop where User answers and Gemini critiques.

## 4. Best Practices

### A. Agent Design
*   **Single Responsibility**: Each agent should do one thing well.
*   **Structured Output**: Use JSON mode in Gemini to ensure agents return data that code can parse (not just chatty text).
*   **Prompt Engineering**: Externalize prompts to `config/prompts.yaml`. Don't hardcode them in Python.

### B. Data & Context
*   **State Management**: Keep the `context/` directory clean. Use Pydantic models to validate data before saving to JSON.
*   **Privacy**: Do not commit personal PII (CVs) to Git. Add `context/*.json` and `context/*.pdf` to `.gitignore`.

### C. Error Handling
*   **API Limits**: Implement backoff/retry logic for Gemini API calls.
*   **Validation**: Always check if the parsed CV JSON has required fields before proceeding.

### D. Development Workflow (Iterative)
1.  **MVP**: Manual Copy-Paste Job Description -> Generate Cover Letter.
2.  **V2**: Upload CV -> Auto-Match.
3.  **V3**: Full Automation with Tracking.

## 5. Next Steps for Developer

1. [ ] Initialize the Git repository and `.gitignore`.
2. [ ] Create the folder structure defined in Section 2.
3. [ ] Implement `tools/gemini_client.py` to establish the AI connection.
4. [ ] Build the `Profile Agent` to parse a dummy CV.
