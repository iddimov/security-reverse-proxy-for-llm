# Test Cases: Security & API

## Overview
The LLM Guardian Proxy is heavily tested with rigorous security boundary edge-cases to guarantee the safety of information before traversing to an external LLM. The automated suite, `test_api.py`, uses Pytest and Playwright.

## Technology Stack
* **Test Runner:** Pytest
* **HTTP Client Request Context:** Playwright Sync API

## Test Categories

### Operational Health
* **`test_health_check`**
  * **Objective:** Verify the proxy server is up and reachable.
  * **Condition:** Sends a `GET` request to the base URL (`/`).
  * **Expected Result:** Connection is established. It doesn't need to return success, just a status code `< 500`.

### Valid Standard Interactions
* **`test_safe_request_passes`**
  * **Objective:** Verify that arbitrary questions (no secrets, no PII) successfully traverse the reverse proxy to the upstream LLM.
  * **Condition:** Sends `{"prompt": "What are the benefits of using FastAPI?"}` to `/v1/proxy`.
  * **Expected Result:** `200 OK`. The payload includes a `status` and the LLM `response`.

### Lexical Boundary Refusals
* **`test_pii_leakage_blocked`**
  * **Objective:** Verify the Presidio lexical layer triggers correctly.
  * **Condition:** Sends a standard sentence containing a phone number and full name.
  * **Expected Result:** Blocked by the Lexical layer. Status `403 Forbidden` with the text: `PII Detected`.

### Semantic Knowledge Leakage Refusals
* **`test_semantic_leakage_blocked`**
  * **Objective:** Verify the TF-IDF Vectorizer layer successfully flags known domain secrets.
  * **Condition:** Prompts the proxy about "Project Phoenix".
  * **Expected Result:** Blocked by the Semantic layer. Status `403 Forbidden` with the text containing `Semantic Similarity`.

### Adversarial Jailbreak Deflection
* **`test_adversarial_jailbreak_blocked`**
  * **Objective:** Verify that slightly obfuscated or "jailbroken" prompts attempting to ask about internal IP addresses or secrets still trigger the vector threshold.
  * **Condition:** Submits an obfuscated inquiry about "that internal thing called Phoenix".
  * **Expected Result:** The semantic similarity remains tight enough (`> 0.85`) to trigger the lock, rejecting with status `403 Forbidden`.

## Running the Tests
```bash
uv run pytest tests/test_api.py -v
```
To run tests locally, ensure the local proxy server is running independently in the background:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
