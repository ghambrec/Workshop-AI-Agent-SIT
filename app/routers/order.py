from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent import order_agent
from app.services.database import write_order

router = APIRouter(prefix="/order")

class UserQuery(BaseModel):
    emailBody: str

@router.post("/create")
async def create_order(query: UserQuery):
    """Creates an order"""
    result = await order_agent.run(query.emailBody)
    write_order(result.output)
    return result.output
