# app/main.py
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.routers.assistant import router


app = FastAPI(title="Retail Agent API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
