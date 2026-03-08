# Feature: Semantic Safety (Vector Similarity)

## Overview
The **Semantic Safety** layer is the second line of defense in the LLM Guardian Proxy. It is specifically designed to detect the leakage of internal secrets, RAG (Retrieval-Augmented Generation) context, or sensitive system prompts that might not be caught by standard PII lexical checks.

## Technology Stack
* **Library:** Scikit-Learn
* **Algorithms:** `TfidfVectorizer`, `cosine_similarity`

## How it Works
1. The system maintains a "Secret Knowledge Base" which contains internal sensitive facts (e.g., project code names, API keys, internal network topology).
2. The user's incoming prompt and the secrets are vectorized into mathematical representations using Term Frequency-Inverse Document Frequency (TF-IDF).
3. Using `cosine_similarity`, the layer calculates the semantic closeness of the prompt to the known internal secrets.
4. If the Cosine Similarity score exceeds the threshold (`> 0.85`), the request is determined to be attempting to extract or discuss internal secrets, and is blocked.

## Why use Semantic Vectors?
This method effectively prevents **"jailbreaking"**. An adversarial user might perfectly paraphrase a request without triggering standard regex/keyword drops (e.g., instead of asking "What is the IP?", they might ask "Can you detail the numbers used for our internal server's network location?"). Semantic vectors catch the *meaning* rather than just the *words*.

## Code Implementation
```python
def semantic_scan(self, text: str):
    """Calculates similarity against internal secrets."""
    if not text: return 0.0
    docs = self.secrets + [text]
    tfidf = self.vectorizer.fit_transform(docs)
    score = cosine_similarity(tfidf[-1], tfidf[:-1]).max()
    return float(score)
```

## Relevant Endpoints
* `POST /v1/proxy`: Evaluates the prompt via `semantic_scan`. If flagged, it returns `403 Forbidden - Security Violation: High Semantic Similarity (score)`.
