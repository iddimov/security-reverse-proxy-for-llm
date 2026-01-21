from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel

from .config import Config
from .security import SecurityService

# Validate configuration
Config.validate()

app = FastAPI(title="LLM Guardian Proxy")
security = SecurityService()
client = genai.Client(api_key=Config.GEMINI_API_KEY)

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
            model=Config.GEMINI_MODEL,
            contents=request.prompt
        )
        return {"status": "success", "response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))