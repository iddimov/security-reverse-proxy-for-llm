# LLM Guardian Proxy Documentation

Welcome to the documentation for the **LLM Guardian Proxy**, a production-ready security reverse proxy designed to sit between internal applications and external Large Language Models (like Google Gemini).

## Overview
Unlike traditional firewalls, LLM Guardian implements **Confidentiality as Code** by performing a dual-layered scanning process before any prompt is forwarded to the LLM.

## Documentation Sections

### Features
* [Lexical Safety (PII Detection)](features/lexical_safety.md)
* [Semantic Safety (Secret Knowledge Leakage)](features/semantic_safety.md)
* [API & LLM Proxy](features/api_proxy.md)

### Test Cases
* [Security & API Tests](test_cases/security_tests.md)
