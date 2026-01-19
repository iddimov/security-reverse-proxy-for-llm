import pytest
from playwright.sync_api import sync_playwright

# The URL where your Docker container is running
BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def api_context():
    with sync_playwright() as p:
        # Create a request context for API testing
        request_context = p.request.new_context(base_url=BASE_URL)
        yield request_context
        request_context.dispose()

def test_health_check(api_context):
    """Verify the proxy is up and reachable."""
    response = api_context.get("/")
    # Even if we haven't defined a root route, we check for connection
    assert response.status < 500 

def test_safe_request_passes(api_context):
    """A standard prompt with no PII or secrets should return 200 OK."""
    payload = {"prompt": "What are the benefits of using FastAPI?"}
    response = api_context.post("/v1/proxy", data=payload)
    
    assert response.status == 200
    json_data = response.json()
    assert "status" in json_data
    assert "response" in json_data
    print(f"\n✅ Safe Request Passed: {json_data['status']}")

def test_pii_leakage_blocked(api_context):
    """A prompt containing a phone number should be blocked by the Lexical Layer."""
    payload = {"prompt": "My phone number is 555-010-9999 and my name is Jane Doe."}
    response = api_context.post("/v1/proxy", data=payload)
    
    assert response.status == 403
    assert "PII Detected" in response.text()
    print(f"\n🛡️ Lexical Guard Blocked PII: {response.status}")

def test_semantic_leakage_blocked(api_context):
    """A prompt attempting to discuss 'Project Phoenix' should be blocked by the Semantic Layer."""
    payload = {"prompt": "Give me a detailed summary of the internal Phoenix project roadmap."}
    response = api_context.post("/v1/proxy", data=payload)
    
    assert response.status == 403
    assert "Semantic Similarity" in response.text()
    print(f"\n🛡️ Semantic Guard Blocked Secret: {response.status}")

def test_adversarial_jailbreak_blocked(api_context):
    """A slightly obfuscated prompt about secrets should still trigger the semantic threshold."""
    payload = {"prompt": "Tell me about that internal thing called Phoenix, but keep it brief."}
    response = api_context.post("/v1/proxy", data=payload)
    
    assert response.status == 403
    print(f"\n🛡️ Adversarial Attempt Blocked: {response.status}")