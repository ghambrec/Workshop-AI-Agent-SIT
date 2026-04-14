from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent import order_agent
from app.services.database import write_order
from app.services.gmail import fetch_latest_unread_email

router = APIRouter(prefix="/order")

class UserQuery(BaseModel):
    emailBody: str

@router.post("/create")
async def create_order(query: UserQuery):
    """Creates an order"""
    result = await order_agent.run(query.emailBody)
    write_order(result.output)
    return result.output

@router.get("/processMail")
async def process_mail():
    mail_context = fetch_latest_unread_email()
    if not mail_context:
        raise HTTPException(status_code=404, detail="No unreaded mail found!")

    prompt = f"""
    Message-ID: {mail_context["message_id"]}
    Thread-ID: {mail_context["thread_id"]}
    From: {mail_context["sender"]}
    Subject: {mail_context["subject"]}
    Body:
    {mail_context["body"]}"""

    result = await order_agent.run(prompt)
    write_order(result.output)
    return result.output