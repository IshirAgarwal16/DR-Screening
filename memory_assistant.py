
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

app = FastAPI(title="DR Screening Memory Assistant")

bank_id = os.getenv("HINDSIGHT_BANK_ID")
hindsight_url = os.getenv("HINDSIGHT_API_URL")
hindsight_key = os.getenv("HINDSIGHT_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not all([bank_id, hindsight_url, hindsight_key, groq_key]):
    raise RuntimeError("Missing required environment variables in .env")

memory = Hindsight(
    base_url=hindsight_url,
    api_key=hindsight_key,
)

llm = Groq(api_key=groq_key)


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.get("/health")
def health():
    return {"status": "healthy", "service": "DR Memory Assistant"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        user_id = request.user_id.strip()
        message = request.message.strip()

        if not user_id or not message:
            raise HTTPException(
                status_code=400,
                detail="user_id and message are required",
            )

        # Retrieve relevant previous memories.
        recalled = memory.recall(
            bank_id=bank_id,
            query=f"Relevant history for user {user_id}: {message}",
        )

        memory_text = "\n".join(
            item.text for item in recalled.results
        ) or "No relevant previous memories found."

        response = llm.chat.completions.create(
            model=groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a DR screening workflow assistant. "
                        "Use the recalled context only as historical "
                        "information. Never invent patient records or "
                        "claim that memory proves a medical diagnosis. "
                        "If information is missing, say so. "
                        "Do not replace professional medical advice."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"User ID: {user_id}\n"
                        f"Recalled context:\n{memory_text}\n\n"
                        f"Question: {message}"
                    ),
                },
            ],
        )

        answer = response.choices[0].message.content

        # Save this interaction for future recall.
        memory.retain(
            bank_id=bank_id,
            content=(
                f"User/session {user_id} asked: {message}\n"
                f"Assistant answered: {answer}"
            ),
            context="DR screening assistant interaction",
        )

        return {
            "success": True,
            "answer": answer,
            "recalled_memories": [
                item.text for item in recalled.results
            ],
        }

    except HTTPException:
        raise
    except Exception as exc:
        print(f"Memory assistant error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Assistant request failed. Check server logs.",
        )


@app.on_event("shutdown")
def shutdown():
    memory.close()
