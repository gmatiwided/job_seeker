"""
Job Seeker Agent
================
An intelligent agent that evaluates job offers against a candidate profile,
and if suitable, generates all application materials (CV, cover letter, interview prep).

Workflow:
1. Assess job match against profile
2. If good match (>60%): Generate CV → Cover Letter → Interview Prep
3. If poor match: Provide feedback and stop
4. Save all materials in job-specific folder
"""

from typing import Annotated, Sequence, TypedDict
from pathlib import Path
import yaml
import json
from datetime import datetime
import re

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

# Import our custom tools
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.cv_generator import CVGeneratorTool
from tools.job_assessment_tool import JobAssessmentTool
from tools.cover_letter_generator import CoverLetterGeneratorTool
from tools.interview_prep_generator import InterviewPrepTool
from tools.pdf_converter import PDFConverterTool

# API Key
api_key = 'AIzaSyAYY4TTtVcOjisOt6nFcx0xppSyBCUKayo'

class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int
    tools_called: list  # Track which tools have been called
    job_folder: str  # Path to the job-specific folder

# Initialize tools (PDF converter will be called directly, not by agent)
assess_job_tool = JobAssessmentTool()
generate_cv_tool = CVGeneratorTool()
generate_cover_letter_tool = CoverLetterGeneratorTool()
generate_interview_prep_tool = InterviewPrepTool()
# pdf_converter_tool - Don't give to agent, we'll call it ourselves after saving files

tools = [assess_job_tool, generate_cv_tool, generate_cover_letter_tool, generate_interview_prep_tool]

# Create LLM class
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
    google_api_key=api_key,
)

# Bind tools to the model
model = llm.bind_tools(tools)

tools_by_name = {tool.name: tool for tool in tools}

# System instruction for the agent
SYSTEM_INSTRUCTION = """You are a professional job application assistant. Your role is to help candidates apply to jobs strategically.

WORKFLOW (MUST FOLLOW IN ORDER - DO NOT REPEAT STEPS):
1. assess_job_match - Evaluate if the job matches the candidate's profile
2. Check the match_score from the assessment:
   - If match_score >= 60: Continue to step 3
   - If match_score < 60: STOP and explain why the job isn't a good fit. DO NOT GENERATE ANY MATERIALS.
3. If match_score >= 60, generate materials in this EXACT order (CALL EACH TOOL ONLY ONCE):
   a) generate_cv - Create tailored CV
   b) generate_cover_letter - Create cover letter
   c) generate_interview_prep - Create interview guide

4. After completing step 3c (interview prep), you are DONE. Provide a summary and STOP.

CRITICAL RULES:
- DO NOT call the same tool multiple times
- DO NOT skip any steps
- Each tool should be called exactly once
- If match score is low (<60), do NOT generate any materials
- After generating all materials (assessment, CV, cover letter, interview prep), STOP immediately

STOPPING CONDITION:
You are finished when you have:
✓ Called assess_job_match once
✓ If match >= 60: Called generate_cv once, generate_cover_letter once, and generate_interview_prep once
✓ If match < 60: Explained why and stopped

Note: PDF conversion will be handled automatically after you finish.

Remember: Quality over quantity. Follow the workflow exactly once."""


# Define our tool node
def call_tool(state: AgentState):
    """Execute tool calls and return results"""
    outputs = []
    tools_called = state.get("tools_called", [])
    
    for tool_call in state["messages"][-1].tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        print(f"\n🔧 Calling tool: {tool_name}")
        
        # Track tool calls - each tool should be called only once
        if tool_name in tools_called:
            print(f"⚠️  Warning: {tool_name} already called, skipping duplicate")
            continue
        tools_called.append(tool_name)
        
        try:
            tool_result = tools_by_name[tool_name].invoke(tool_args)
            
            outputs.append(
                ToolMessage(
                    content=str(tool_result),
                    name=tool_name,
                    tool_call_id=tool_call["id"],
                )
            )
            print(f"✅ Tool {tool_name} completed")
        except Exception as e:
            error_msg = f"Error in {tool_name}: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            outputs.append(
                ToolMessage(
                    content=error_msg,
                    name=tool_name,
                    tool_call_id=tool_call["id"],
                )
            )
    
    return {"messages": outputs, "tools_called": tools_called}


def call_model(state: AgentState, config: RunnableConfig):
    """Call the LLM with current state"""
    response = model.invoke(state["messages"], config)
    return {"messages": [response]}


def should_continue(state: AgentState):
    """Determine whether to continue or end"""
    messages = state["messages"]
    last_message = messages[-1]
    tools_called = state.get("tools_called", [])
    
    # Check if we've completed all necessary tools for a good match
    has_assessment = "assess_job_match" in tools_called
    has_cv = "generate_cv" in tools_called
    has_cover = "generate_cover_letter" in tools_called
    has_interview = "generate_interview_prep" in tools_called
    
    # If we have all the materials, we're done
    if has_assessment and has_cv and has_cover and has_interview:
        print("\n✅ All materials generated, workflow complete!")
        return "end"
    
    # Safety check: prevent infinite loops (max 8 tool calls now - no PDF conversion)
    if len(tools_called) > 8:
        print("\n⚠️  Max tool calls reached, ending workflow")
        return "end"
    
    # If the last message has tool calls, continue
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    
    # Otherwise end
    return "end"


# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("llm", call_model)
workflow.add_node("tools", call_tool)

# Set entry point
workflow.set_entry_point("llm")

# Add conditional edges
workflow.add_conditional_edges(
    "llm",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

# Add edge back to llm after tools
workflow.add_edge("tools", "llm")

# Compile the graph
graph = workflow.compile()


def load_profile() -> str:
    """Load candidate profile from YAML"""
    profile_path = Path(__file__).parent.parent / "config" / "profile.yaml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile_data = yaml.safe_load(f)
    return yaml.dump(profile_data)


def sanitize_folder_name(job_title: str, company: str = None) -> str:
    """Create a safe folder name from job title and company"""
    # Remove special characters and replace spaces with underscores
    safe_title = re.sub(r'[^\w\s-]', '', job_title).strip().replace(' ', '_')
    if company:
        safe_company = re.sub(r'[^\w\s-]', '', company).strip().replace(' ', '_')
        folder_name = f"{safe_company}_{safe_title}"
    else:
        folder_name = safe_title
    
    # Add timestamp to make unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{folder_name}_{timestamp}"


def save_application_materials(job_folder: Path, messages: Sequence[BaseMessage]):
    """Extract and save all generated materials from agent messages, then convert to PDF"""
    print(f"\n💾 Saving materials to: {job_folder}")
    
    # Import PDF converter
    from tools.pdf_converter import convert_txt_to_pdf
    
    assessment = None
    cv = None
    cover_letter = None
    interview_prep = None
    
    # Extract tool results from messages
    for msg in messages:
        if isinstance(msg, ToolMessage):
            content = msg.content
            
            if msg.name == "assess_job_match":
                assessment = content
                # Save assessment
                assessment_file = job_folder / "assessment.json"
                assessment_file.write_text(content, encoding='utf-8')
                print(f"  ✓ Assessment saved")
            
            elif msg.name == "generate_cv":
                cv = content
                cv_file = job_folder / "cv.txt"
                cv_file.write_text(content, encoding='utf-8')
                print(f"  ✓ CV saved (txt)")
            
            elif msg.name == "generate_cover_letter":
                cover_letter = content
                cover_file = job_folder / "cover_letter.txt"
                cover_file.write_text(content, encoding='utf-8')
                print(f"  ✓ Cover letter saved (txt)")
            
            elif msg.name == "generate_interview_prep":
                interview_prep = content
                interview_file = job_folder / "interview_prep.md"
                interview_file.write_text(content, encoding='utf-8')
                print(f"  ✓ Interview prep saved")
    
    # Now convert txt files to PDF
    print(f"\n📄 Converting to PDF...")
    cv_pdf_exists = False
    cover_pdf_exists = False
    
    # Convert CV to PDF
    if cv:
        cv_txt = job_folder / "cv.txt"
        cv_pdf = job_folder / "cv.pdf"
        if cv_txt.exists():
            result = convert_txt_to_pdf(str(cv_txt), str(cv_pdf), "cv")
            print(f"  {result}")
            cv_pdf_exists = cv_pdf.exists()
    
    # Convert cover letter to PDF
    if cover_letter:
        cover_txt = job_folder / "cover_letter.txt"
        cover_pdf = job_folder / "cover_letter.pdf"
        if cover_txt.exists():
            result = convert_txt_to_pdf(str(cover_txt), str(cover_pdf), "cover_letter")
            print(f"  {result}")
            cover_pdf_exists = cover_pdf.exists()
    
    print(f"\n✅ All materials saved in: {job_folder.name}")
    
    # Summary - check actual files
    print(f"\n📄 Files created:")
    for file in sorted(job_folder.iterdir()):
        if file.is_file():
            size_kb = file.stat().st_size / 1024
            file_type = "📋" if file.suffix == ".txt" else "📄" if file.suffix == ".pdf" else "📊" if file.suffix == ".json" else "📝"
            print(f"   {file_type} {file.name} ({size_kb:.1f} KB)")
    
    return {
        "assessment": assessment,
        "cv": cv,
        "cover_letter": cover_letter,
        "interview_prep": interview_prep,
        "cv_pdf": cv_pdf_exists,
        "cover_letter_pdf": cover_pdf_exists
    }


def process_job_application(job_offer: str, job_title: str = None, company: str = None):
    """
    Main function to process a job application through the agent.
    
    Args:
        job_offer: The job description/offer text
        job_title: Optional job title for folder naming
        company: Optional company name for folder naming
    
    Returns:
        Dictionary with all generated materials and their file paths
    """
    print("=" * 70)
    print("🎯 JOB SEEKER AGENT - Starting Application Process")
    print("=" * 70)
    
    # Load profile
    profile = load_profile()
    
    # Extract job title from offer if not provided
    if not job_title:
        # Simple extraction - look for common patterns
        lines = job_offer.split('\n')
        job_title = lines[0] if lines else "Job_Application"
    
    # Create job-specific folder
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    folder_name = sanitize_folder_name(job_title, company)
    job_folder = output_dir / folder_name
    job_folder.mkdir(exist_ok=True)
    
    print(f"\n📁 Job folder created: {folder_name}")
    
    # Save the job offer
    job_offer_file = job_folder / "job_offer.txt"
    job_offer_file.write_text(job_offer, encoding='utf-8')
    print(f"  ✓ Job offer saved")
    
    # Create initial messages with system instruction
    initial_messages = [
        SystemMessage(content=SYSTEM_INSTRUCTION),
        HumanMessage(content=f"""I need your help applying to this job. Please evaluate if it's a good match for my profile, and if so, generate all necessary application materials.

CANDIDATE PROFILE:
{profile}

JOB OFFER:
{job_offer}

Please start by assessing the job match, then proceed accordingly. Generate CV, cover letter, and interview prep materials if it's a good match.""")
    ]
    
    # Initialize state
    initial_state = {
        "messages": initial_messages,
        "number_of_steps": 0,
        "tools_called": [],
        "job_folder": str(job_folder)
    }
    
    print("\n🤖 Agent processing job application...")
    print("-" * 70)
    
    # Run the agent
    final_state = graph.invoke(initial_state)
    
    print("-" * 70)
    
    # Save all materials
    materials = save_application_materials(job_folder, final_state["messages"])
    
    # Add folder path to results
    materials["job_folder"] = str(job_folder)
    materials["folder_name"] = folder_name
    
    print("\n" + "=" * 70)
    print("✅ APPLICATION PROCESS COMPLETE")
    print("=" * 70)
    
    return materials

