from fastapi import APIRouter
from pydantic import BaseModel
from pydantic_ai.messages import ModelMessage
from app.services.agent import order_agent

router = APIRouter(prefix="/order")

# --- IN-MEMORY CHAT DATABASE ---
# For the workshop demo, we use a simple dictionary to remember conversations.
# In a real app, you would save this to Redis or Postgres.
# chat_sessions: dict[str, list[ModelMessage]] = {}


class UserQuery(BaseModel):
    emailBody: str


# @router.get("/welcome/{session_id}")
# async def welcome_message(session_id: str):
#     """Initializes a new chat session and returns the welcome greeting."""
#     # Create an empty history list for this new session
#     chat_sessions[session_id] = []

#     return {
#         "session_id": session_id,
#         "message": (
#             "Welcome to the Store Manager Portal! 👋\n"
#             "I can help you analyze product performance, identify our best sellers, "
#             "and automatically place restock orders for low inventory. "
#             "What would you like to check today?"
#         ),
#     }


# @router.post("/ask")
# async def ask_assistant(query: UserQuery):
#     """Processes a message while remembering previous context."""

#     # 1. Fetch the conversation history for this specific session
#     # If the session doesn't exist, we start with an empty list
#     history = chat_sessions.get(query.session_id, [])

#     # 2. Run the agent, passing in the history so it remembers the chat
#     result = await order_agent.run(query.prompt, message_history=history)

#     # 3. Save the newly updated history back into our dictionary
#     # result.all_messages() contains the old history PLUS the new request/response
#     chat_sessions[query.session_id] = result.all_messages()

#     # 4. Return the structured output
#     return result.output

@router.post("/create")
async def create_order(query: UserQuery):
    """Creates an order"""
    result = await order_agent.run(query.emailBody)
    return result.output
