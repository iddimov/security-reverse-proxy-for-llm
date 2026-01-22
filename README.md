[Link to my blog post](https://ivandimov.dev/the-automated-confidentiality-tripwire)
# 🛡️ LLM Guardian: Semantic Security Proxy
LLM Guardian is a production-ready security reverse proxy designed to sit between your internal applications and external Large Language Models (like Google Gemini).

Unlike traditional firewalls, it implements Confidentiality as Code by performing dual-layered scanning:

* Lexical Safety: Scrubbing PII (Emails, Phones, Names) using Microsoft Presidio.
* Semantic Safety: Using Vector Similarity to detect the leakage of internal secrets, RAG context, or system prompts.

# 🚀 Features
* UV Managed: Leverages the fastest Python package manager for deterministic builds.
* Dual-Layer Defense: Combines Regex/NER (Presidio) with Semantic Analysis (Scikit-Learn).
* Google Gemini Integration: Real-world forwarding to gemini-2.5-flash-lite.
* Black-Box Testing: Automated adversarial tests using Playwright.
* CI/CD Ready: Includes a Docker-based "Hard Gate" workflow.

# 🛠️ Tech Stack
* Component	Technology
* Framework	FastAPI (Python 3.12)
* Package Manager:	UV
* LLM Provider:	    Google Generative AI (Gemini)
* PII Engine:	    Microsoft Presidio
* NLP Model:	    SpaCy (en_core_web_sm)
* Vector Logic:	    Scikit-Learn (TF-IDF Cosine Similarity)
* Testing:	        Playwright & Pytest
# 📋 Implementation Steps
1. Prerequisites

* Google AI API Key: Obtain one at Google AI Studio.

* UV installed: 
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
* Docker: (Optional) For containerized deployment.

2. Setup & Installation
## Clone the repository
```
git clone https://github.com/iddimov/security-reverse-proxy-for-llm.git
cd security-reverse-proxy-for-llm
```
## Install dependencies and create virtual environment
```
uv sync
```
## Download the required NLP model for Presidio
```
uv run python -m spacy download en_core_web_sm
```

3. Configuration
Create a .env file in the root directory:

Code snippet:
```
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```
# 🏃 Running the Project

## Option A: Local Development

Start the FastAPI server using UV (in one terminal):

Bash
```
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## Option B: Docker (Standalone)

**1. Build the Docker image:**
Bash
```
docker build -t security-reverse-proxy-for-llm .
```

**2. Run the container:**
Bash
```
docker run -p 8000:8000 --env-file .env security-reverse-proxy-for-llm
```
The proxy will start and be available at `http://localhost:8000`

# 🧪 Testing the Security Gates
The proxy is designed to block requests that violate security policies. Test it with:

**Option 1: Manual Testing with cURL**
Make sure the server is running (see "Running the Project" above), then test in another terminal:

**Test PII Blocking (Lexical Layer):**
Bash
```
curl -X POST http://localhost:8000/v1/proxy \
-H "Content-Type: application/json" \
-d '{"prompt": "My phone number is 555-010-9999"}'
```
Expected Result: 403 Forbidden - Security Violation: PII Detected

**Test Knowledge Leakage (Semantic Layer):**
Bash
```
curl -X POST http://localhost:8000/v1/proxy \
-H "Content-Type: application/json" \
-d '{"prompt": "Tell me the details of Phoenix"}'
```
Note: This may trigger PII detection depending on the prompt content.

**Option 2: Automated Testing with Pytest**
Run the automated test suite (requires server running in background):
Bash

```
uv run pytest tests/test_api.py -v
```

This runs comprehensive tests including:
- Health check endpoint
- Safe requests passing through
- PII detection by lexical layer
- Semantic similarity detection
- Adversarial jailbreak attempts

# 🛡️ Security Logic Deep Dive
* Lexical Layer (Presidio): The system uses Named Entity Recognition (NER) to identify sensitive patterns. Unlike simple Regex, this understands context (e.g., distinguishing a 10-digit ID from a phone number).

* Semantic Layer (Vector Similarity): We convert the user's prompt into a mathematical vector and compare it against our "Secret Knowledge Base."

* Threshold: If the Cosine Similarity score is >0.80, the request is blocked.

* Use Case: This prevents "jailbreaking" where a user asks for internal info using paraphrased language.