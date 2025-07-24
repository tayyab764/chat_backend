# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json
import os

from gemini_client import ask_gemini  # 💡 Using Gemini model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_log_path = "chat_log.json"

# Init chat log
if not os.path.exists(chat_log_path):
    with open(chat_log_path, "w") as f:
        json.dump([], f)

class Message(BaseModel):
    message: str

@app.post("/ask")
async def ask_question(msg: Message):
    user_message = msg.message
    try:
        response = ask_gemini(user_message)  # ✅ Real Gemini response
    except Exception as e:
        response = f"Error: {str(e)}"

    # Save to log
    with open(chat_log_path, "r") as f:
        history = json.load(f)
    history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_message,
        "bot": response
    })
    with open(chat_log_path, "w") as f:
        json.dump(history, f, indent=2)

    return {"response": response}

@app.get("/history")
def get_history():
    with open(chat_log_path, "r") as f:
        return json.load(f)
