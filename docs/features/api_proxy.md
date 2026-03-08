# Feature: API & Proxy

## Overview
The heart of the application is a **FastAPI** service which acts as the actual proxy endpoint (`/v1/proxy`). It handles incoming requests, orchestrates the two security layers (Lexical and Semantic), and if authorized, forwards the request securely to the upstream LLM (Google Gemini).

## Technology Stack
* **Framework:** FastAPI
* **LLM Provider:** Google Generative AI (`genai`)
* **Data Validation:** Pydantic

## How it Works
1. Validates the incoming configuration (e.g., ensuring `GEMINI_API_KEY` and `GEMINI_MODEL` are set).
2. Starts up a FastAPI instance and instantiates the `SecurityService`.
3. Sets up a Google GenAI Client with the secured API Key.
4. An endpoint `POST /v1/proxy` is exposed. This endpoint accepts JSON conforming to the `PromptRequest` schema (a simple wrapper around the input text).
5. The endpoint logic acts as a sequence of hard gates:
    - **Step 1:** The prompt passes through `lexical_scan(prompt)`. It immediately raises a `403` if PII is found.
    - **Step 2:** The prompt passes through `semantic_scan(prompt)`. It immediately raises a `403` if similarity exceeds 0.85 against secrets.
    - **Step 3:** The request reaches `generate_content` and calls `gemini-2.5-flash-lite`, successfully responding with the LLM's generated text.

## Code Implementation
`app.main` acts as the secure entrypoint:

```python
@app.post("/v1/proxy")
async def secure_llm_call(request: PromptRequest):
    # Lexical Guard
    if security.lexical_scan(request.prompt):
        raise ...
        
    ... # Semantic Guard

    # Authorized Forwarding
    response = client.models.generate_content(...)
    return {"status": "success", "response": response.text}
```

## Relevant Endpoints
* `POST /v1/proxy`: Submits prompt to LLM after dual-layer security scan.
