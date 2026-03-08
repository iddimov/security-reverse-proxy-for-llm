# Feature: Lexical Safety (PII Detection)

## Overview
The **Lexical Safety** layer acts as the first line of defense for the LLM Guardian Proxy. It is responsible for scrubbing and detecting Personally Identifiable Information (PII) before it leaves the internal network.

## Technology Stack
* **Engine:** Microsoft Presidio (`presidio_analyzer`, `presidio_anonymizer`)
* **NLP Model:** SpaCy (`en_core_web_sm`)

## How it Works
1. When a user submits a prompt, it is passed through the `lexical_scan` method in the `SecurityService`.
2. The `AnalyzerEngine` analyzes the text using Named Entity Recognition (NER). Unlike simple regular expressions, Presidio understands context, making it much more accurate (e.g., distinguishing a 10-digit employee ID from a phone number).
3. If the engine confidently detects any PII (score > 0.8), the request is immediately flagged and blocked.

## Code Implementation
```python
def lexical_scan(self, text: str):
    """Returns True if high-confidence PII is detected."""
    results = self.analyzer.analyze(text=text, entities=None, language='en')
    return any(r.score > 0.8 for r in results)
```

## Relevant Endpoints
* `POST /v1/proxy`: The prompt is checked via `lexical_scan` before any further processing. If flagged, it returns `403 Forbidden - Security Violation: PII Detected`.
