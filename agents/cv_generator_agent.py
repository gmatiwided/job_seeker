"""
CV Generator Agent using LangGraph and Google Gemini
This agent takes a job offer and generates an ATS-optimized plain text CV with job assessment
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
import yaml
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import tools from the tools package
from tools import generate_cv, assess_job_match

# Read API key
API_KEY = 'AIzaSyAYY4TTtVcOjisOt6nFcx0xppSyBCUKayo'


class AgentState(TypedDict):
    """The state of the CV generator agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    job_offer: str
    user_profile: dict


def load_user_profile(profile_path: str = "build_with_ai/config/profile.yaml") -> dict:
    """Load user profile from YAML file"""
    try:
        with open(profile_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading profile: {e}")
        return {}


class CVGeneratorAgent:
    """LangGraph agent for ATS-optimized CV generation"""
    
    # ATS-Optimized CV Generation System Prompt
    SYSTEM_PROMPT = """You are a professional CV writer and ATS optimization expert.

Your task is to generate an ATS-friendly CV in PLAIN TEXT (.txt format only) based strictly on:
1) The provided candidate profile details
2) The provided job description

CRITICAL RULES (MUST FOLLOW):
- DO NOT invent, assume, exaggerate, or infer any information.
- DO NOT add skills, tools, experience, metrics, certifications, or achievements that are not explicitly mentioned in the profile details.
- If a required section has no relevant information, omit the section entirely.
- Do NOT use tables, columns, graphics, icons, emojis, or special characters.
- Use simple, ATS-compatible formatting only.
- Use standard job-relevant keywords ONLY if they already appear in the profile or job description.
- Do NOT include personal opinions, summaries, or explanations outside the CV content.

OUTPUT FORMAT:
- Plain text (.txt)
- No markdown formatting (no #, **, *, etc.)
- No bullet symbols other than hyphens (-)
- One page where possible
- Clean spacing and clear section headers

CV STRUCTURE (USE THIS ORDER):

NAME
Job Title (aligned with job description, if supported by profile)
City, Country | Email | Phone | LinkedIn | GitHub (only if provided)

PROFESSIONAL SUMMARY
- 2-3 concise lines
- Written strictly from the provided profile
- Aligned to the job description without adding new facts

SKILLS
- List skills exactly as provided
- Group logically if applicable (e.g., Technical Skills, Tools)

PROFESSIONAL EXPERIENCE
Job Title - Company Name
Location | Start Date - End Date
- Achievement or responsibility (fact-based, no assumptions)
- Use action verbs but no fabricated metrics

(Repeat for all roles provided)

PROJECTS (ONLY IF PROVIDED)
Project Name
- Brief description based strictly on given details
- Technologies used (only if explicitly mentioned)

EDUCATION
Degree - Field of Study
Institution Name | Location | Graduation Year (if provided)

CERTIFICATIONS (ONLY IF PROVIDED)
- Certification Name - Issuing Organization - Year

ADDITIONAL INFORMATION (OPTIONAL)
- Languages
- Publications
- Volunteer experience
(Only include if explicitly provided)

TOOLS AVAILABLE:
1. assess_job_match - Analyzes candidate fit for the job
2. generate_cv - Generates the ATS-friendly CV

YOU MUST:
1. First call assess_job_match with the job offer and user profile
2. Then call generate_cv with the job offer and user profile
3. After both tools complete, provide a brief summary

Remember: The generate_cv tool will create the properly formatted plain text CV. 
Your job is to call the tools with the correct parameters."""
    
    def __init__(self, api_key: str, profile_path: str = "build_with_ai/config/profile.yaml"):
        self.api_key = api_key
        self.user_profile = load_user_profile(profile_path)
        
        # Create LLM with tools
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=api_key,
        )
        
        # Available tools
        self.tools = [generate_cv, assess_job_match]
        self.tools_by_name = {tool.name: tool for tool in self.tools}
        
        # Bind tools to model
        self.model = self.llm.bind_tools(self.tools)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _call_tool(self, state: AgentState) -> dict:
        """Execute tool calls"""
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=str(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    
    def _call_model(self, state: AgentState, config: RunnableConfig) -> dict:
        """Invoke the model with ATS-focused instructions"""
        # Get profile summary
        name = state["user_profile"].get('name', 'N/A')
        specialty = state["user_profile"].get('specialty', 'N/A')
        
        # Build context message with system prompt
        context_message = f"""{self.SYSTEM_PROMPT}

CANDIDATE PROFILE DATA:
{state["user_profile"]}

User Summary:
- Name: {name}
- Specialty: {specialty}

IMPORTANT INSTRUCTIONS:
1. You have access to two tools: assess_job_match and generate_cv
2. Call assess_job_match first with: job_offer=<job description>, user_profile=<profile dict>
3. Then call generate_cv with the same parameters
4. Both tools require the full user_profile dictionary as a parameter
5. After both tools complete, provide a brief summary

The generate_cv tool will create the ATS-friendly plain text CV according to all the rules above.
Do NOT attempt to format the CV yourself - let the tool handle it.
"""
        
        messages = [HumanMessage(content=context_message)] + state["messages"]
        response = self.model.invoke(messages, config)
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """Determine if we should continue or end"""
        messages = state["messages"]
        if not messages[-1].tool_calls:
            return "end"
        return "continue"
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("llm", self._call_model)
        workflow.add_node("tools", self._call_tool)
        
        # Set entry point
        workflow.set_entry_point("llm")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "llm",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )
        
        # Add edge from tools back to llm
        workflow.add_edge("tools", "llm")
        
        return workflow.compile()
    
    def generate_cv_for_job(self, job_offer: str, verbose: bool = True) -> dict:
        """
        Main method to generate ATS-optimized CV and assessment for a job offer
        
        Args:
            job_offer: The job offer description
            verbose: Whether to print progress
            
        Returns:
            dict with 'cv', 'assessment', and 'final_response' keys
        """
        # Prepare initial message
        initial_message = f"""I need to apply for this job position. Please help me by:

1. Using assess_job_match to analyze how well my profile matches this job
2. Using generate_cv to create an ATS-optimized plain text CV

Remember:
- Pass my complete user_profile as a parameter to both tools
- Do NOT invent or assume any information
- The CV must be in plain text format (no markdown)
- Only use information from my profile

Here is the job offer:

{job_offer}

Please proceed with calling both tools."""
        
        inputs = {
            "messages": [HumanMessage(content=initial_message)],
            "job_offer": job_offer,
            "user_profile": self.user_profile
        }
        
        # Run the graph
        result = {"cv": "", "assessment": "", "messages": [], "final_response": ""}
        
        if verbose:
            print("\n🤖 ATS CV Generator Agent is processing your request...\n")
        
        for state in self.graph.stream(inputs, stream_mode="values"):
            last_message = state["messages"][-1]
            result["messages"] = state["messages"]
            
            if verbose:
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"🔧 Calling tool: {tool_call['name']}")
                elif isinstance(last_message, ToolMessage):
                    print(f"✅ Tool '{last_message.name}' completed")
                elif isinstance(last_message, AIMessage) and last_message.content:
                    print(f"💬 Agent: {last_message.content[:100]}...")
        
        # Extract CV and assessment from messages
        for message in result["messages"]:
            if isinstance(message, ToolMessage):
                if message.name == "generate_cv":
                    result["cv"] = message.content
                    if verbose:
                        print(f"\n📄 ATS CV generated ({len(message.content)} characters)")
                elif message.name == "assess_job_match":
                    result["assessment"] = message.content
                    if verbose:
                        print(f"\n📊 Job assessment completed ({len(message.content)} characters)")
            elif isinstance(message, AIMessage) and message.content and not message.tool_calls:
                result["final_response"] = message.content
        
        return result


def main():
    """Example usage"""
    print("=" * 80)
    print("ATS-OPTIMIZED CV GENERATOR AGENT")
    print("Powered by LangGraph & Google Gemini")
    print("=" * 80)
    
    # Initialize agent
    print("\n📋 Loading user profile...")
    agent = CVGeneratorAgent(api_key=API_KEY)
    
    if not agent.user_profile:
        print("❌ Error: Could not load user profile!")
        return
    
    print(f"✅ Profile loaded for: {agent.user_profile.get('name', 'Unknown')}")
    
    # Example job offer
    job_offer = """
Data Scientist - Junior to Mid Level

We are seeking a talented Data Scientist to join our growing analytics team.

Requirements:
- 2+ years of experience in data science, analytics, or related field
- Strong proficiency in Python (pandas, scikit-learn, NumPy, matplotlib)
- Experience with SQL and database querying
- Knowledge of machine learning algorithms and statistical analysis
- Data visualization skills using Tableau, Power BI, or similar tools
- Strong analytical and problem-solving abilities
- Excellent communication skills

Responsibilities:
- Analyze large datasets to extract meaningful insights
- Build and deploy predictive models for business use cases
- Create dashboards and visualizations for stakeholders
- Collaborate with cross-functional teams
- Present findings to technical and non-technical audiences
- Contribute to data strategy and best practices

Nice to Have:
- Experience in logistics or supply chain domain
- Knowledge of Agile methodologies
- Contributions to data science projects or communities
- R programming skills

Location: Tunisia (Hybrid)
"""
    
    print("\n" + "=" * 80)
    print("JOB OFFER")
    print("=" * 80)
    print(job_offer)
    
    # Generate CV and assessment
    result = agent.generate_cv_for_job(job_offer, verbose=True)
    
    # Display results
    print("\n" + "=" * 80)
    print("📊 JOB MATCH ASSESSMENT")
    print("=" * 80)
    if result.get("assessment"):
        print(result["assessment"])
    else:
        print("⚠️ No assessment generated")
    
    print("\n" + "=" * 80)
    print("📄 ATS-OPTIMIZED CV (PLAIN TEXT)")
    print("=" * 80)
    if result.get("cv"):
        print(result["cv"])
    else:
        print("⚠️ No CV generated")
    
    if result.get("final_response"):
        print("\n" + "=" * 80)
        print("💬 AGENT SUMMARY")
        print("=" * 80)
        print(result["final_response"])
    
    # Save outputs
    output_dir = Path("build_with_ai/agents/output")
    output_dir.mkdir(exist_ok=True)
    
    cv_file = output_dir / "ats_cv.txt"
    assessment_file = output_dir / "job_assessment.txt"
    
    with open(cv_file, "w", encoding="utf-8") as f:
        f.write(result.get("cv", "No CV generated"))
    
    with open(assessment_file, "w", encoding="utf-8") as f:
        f.write(result.get("assessment", "No assessment generated"))
    
    print("\n" + "=" * 80)
    print("💾 FILES SAVED")
    print("=" * 80)
    print(f"📄 ATS CV: {cv_file}")
    print(f"📊 Assessment: {assessment_file}")
    print("\nTo view the files:")
    print(f"  type {cv_file}")
    print(f"  type {assessment_file}")


if __name__ == "__main__":
    main()
