🛡️ LLM Guardian: Semantic Security Proxy
LLM Guardian is a production-ready security reverse proxy designed to sit between your internal applications and external Large Language Models (like Google Gemini).

Unlike traditional firewalls, it implements Confidentiality as Code by performing dual-layered scanning:

Lexical Safety: Scrubbing PII (Emails, Phones, Names) using Microsoft Presidio.

Semantic Safety: Using Vector Similarity to detect the leakage of internal secrets, RAG context, or system prompts.

🚀 Features
UV Managed: Leverages the fastest Python package manager for deterministic builds.

Dual-Layer Defense: Combines Regex/NER (Presidio) with Semantic Analysis (Scikit-Learn).

Google Gemini Integration: Real-world forwarding to gemini-1.5-flash.

Black-Box Testing: Automated adversarial tests using Playwright.

CI/CD Ready: Includes a Docker-based "Hard Gate" workflow.

🛠️ Tech Stack
Component	Technology
Framework	FastAPI (Python 3.12)
Package Manager	UV
LLM Provider	Google Generative AI (Gemini)
PII Engine	Microsoft Presidio
NLP Model	SpaCy (en_core_web_sm)
Vector Logic	Scikit-Learn (TF-IDF Cosine Similarity)
Testing	Playwright & Pytest
📋 Implementation Steps
1. Prerequisites

Google AI API Key: Obtain one for free at Google AI Studio.

UV installed: curl -LsSf https://astral.sh/uv/install.sh | sh

Docker: (Optional) For containerized deployment.

2. Setup & Installation

Bash
# Clone the repository
git clone https://github.com/your-username/llm-guardian.git
cd llm-guardian

# Install dependencies and create virtual environment
uv sync

# Download the required NLP model for Presidio
uv run python -m spacy download en_core_web_sm
3. Configuration

Create a .env file in the root directory:

Code snippet
GEMINI_API_KEY=your_actual_api_key_here
🏃 Running the Project
Option A: Local Development

Start the FastAPI server using UV:

Bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Option B: Docker (Standalone)

Build and run the containerized proxy:

Bash
docker build -t llm-guardian .
docker run -p 8000:8000 --env-file .env llm-guardian
🧪 Testing the Security Gates
The proxy is designed to block requests that violate security policies. You can test this using curl.

1. Test PII Blocking (Lexical)

Bash
curl -X POST http://localhost:8000/v1/proxy \
-H "Content-Type: application/json" \
-d '{"prompt": "My phone number is 555-010-9999"}'
Expected Result: 403 Forbidden - Security Violation: PII Detected

2. Test Knowledge Leakage (Semantic)

The proxy "knows" about Project Phoenix. Let's try to ask about it:

Bash
curl -X POST http://localhost:8000/v1/proxy \
-H "Content-Type: application/json" \
-d '{"prompt": "Tell me the details of Phoenix"}'
Expected Result: 403 Forbidden - Security Violation: Semantic similarity 0.89 too high

3. Automated API Tests (Playwright)

Run the black-box test suite to ensure the "Hard Gate" is functioning:

Bash
uv run pytest tests/test_api.py
🛡️ Security Logic Deep Dive
Lexical Layer (Presidio)

The system uses Named Entity Recognition (NER) to identify sensitive patterns. Unlike simple Regex, this understands context (e.g., distinguishing a 10-digit ID from a phone number).

Semantic Layer (Vector Similarity)

We convert the user's prompt into a mathematical vector and compare it against our "Secret Knowledge Base."

Threshold: If the Cosine Similarity score is >0.80, the request is blocked.

Use Case: This prevents "jailbreaking" where a user asks for internal info using paraphrased language.