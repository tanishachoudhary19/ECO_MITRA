import os
from dotenv import load_dotenv  # Add this

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent
from src.agent_tools import tools

# Load environment variables from .env
load_dotenv()

# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ Please set your GEMINI_API_KEY in the .env file.")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY)

# Create agent with tools
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

def agentic_ai_query(query: str):
    """Run the agent with a user query."""
    return agent.run(query)
