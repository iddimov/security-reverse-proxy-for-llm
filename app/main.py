import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from .security import SecurityService

# Load variables from .env if it exists
load_dotenv()

app = FastAPI(title="LLM Guardian Proxy")
security = SecurityService()

# Retrieve key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=api_key)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/v1/proxy")
async def secure_llm_call(request: PromptRequest):
    # Lexical Guard
    if security.lexical_scan(request.prompt):
        raise HTTPException(status_code=403, detail="Security Violation: PII Detected")

    # Semantic Guard
    sim_score = security.semantic_scan(request.prompt)
    if sim_score > 0.85:
        raise HTTPException(status_code=403, detail=f"Security Violation: High Semantic Similarity ({sim_score:.2f})")

    # Authorized Forwarding
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=request.prompt
        )
        return {"status": "success", "response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))