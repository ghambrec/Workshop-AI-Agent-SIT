import os
from dotenv import load_dotenv

# 1. LOAD THE ENV BEFORE ANYTHING ELSE HAPPENS!
load_dotenv()

from pathlib import Path
from langfuse import get_client
from pydantic_ai import Agent
from app.models.order import AgentResponse
from app.services.gmail import send_mail

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROMPT_DIR = BASE_DIR / "app/prompts"
SOUL_MD = PROMPT_DIR / "soul.md"


langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

Agent.instrument_all()



# INITIALIZE THE AGENT

soul_prompt = Path(SOUL_MD).read_text(encoding="utf-8")

order_agent = Agent(
    "vertexai:gemini-2.5-flash",
    output_type=AgentResponse,
    instrument=True,
    tools=[send_mail],
    system_prompt=soul_prompt,
)
