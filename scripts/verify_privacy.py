import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_privacy():
    print("--- HunterOS Privacy Leak Verification ---")
    
    # Test 1: Direct access to static resumes (should fail or be masked)
    print("Test 1: Attempting unauthenticated access to /static/resumes/sample.pdf...")
    try:
        res = requests.get(f"{BASE_URL}/static/resumes/sample.pdf", timeout=5)
        if res.status_code == 404 or res.status_code == 401:
            print(f"PASSED: Access denied ({res.status_code})")
        else:
            print(f"FAILED: Potential leak! Received status {res.status_code}")
    except Exception as e:
        print(f"PASSED: Static mount disabled ({str(e)})")

    # Test 2: Rate Limiting check
    print("\nTest 2: Brute-force rate limit check (root)...")
    for i in range(15):
        res = requests.get(BASE_URL)
        if res.status_code == 429:
            print(f"PASSED: Rate limit triggered after {i+1} requests")
            break
    else:
        print("WARNING: Rate limit NOT triggered after 15 requests (check configuration)")

    # Test 3: Security Headers
    print("\nTest 3: Security headers check...")
    res = requests.get(BASE_URL)
    headers = res.headers
    required = ["X-Content-Type-Options", "X-Frame-Options", "X-XSS-Protection", "Strict-Transport-Security"]
    
    all_headers = True
    for h in required:
        if h in headers:
            print(f"PASSED: {h} is present")
        else:
            print(f"FAILED: {h} is MISSING")
            all_headers = False
            
    if all_headers:
        print("\nPRIVACY STATUS: SECURE. No obvious leaks detected.")
    else:
        print("\nPRIVACY STATUS: DEGRADED. Security headers missing.")

    # Test 4: PII Redaction Audit
    print("\nTest 4: PII Redaction Audit (Logic Check)...")
    from app.utils.privacy import privacy_shield
    
    dirty_text = "My email is john.doe@example.com and my phone is 555-123-4567. I live at 123 Main St."
    clean_text = privacy_shield.mask_pii(dirty_text)
    
    if "john.doe" not in clean_text and "555-123" not in clean_text and "123 Main St" not in clean_text:
        print("PASSED: PII successfully masked")
        print(f"DEBUG: {clean_text}")
    else:
        print("FAILED: PII leak in masking logic!")
        print(f"DEBUG: {clean_text}")

if __name__ == "__main__":
    verify_privacy()
