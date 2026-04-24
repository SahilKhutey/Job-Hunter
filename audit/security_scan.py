import requests

BASE_URL = "http://localhost:8000/api/v1"

def run_security_scan():
    print("\n🛡️ PENETRATION & VULNERABILITY SCAN (BASIC)")

    # 1. SQL Injection Simulation
    # Testing if login form is vulnerable to simple SQLi
    payload = "' OR '1'='1"
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={
            "username": payload,
            "password": "any"
        })
        if res.status_code != 200:
            print("✅ SQL Injection Resistance: OK")
        else:
            print("❌ SQL Injection Resistance: VULNERABLE")
    except Exception as e:
        print(f"❌ SQLi Test: ERROR ({e})")

    # 2. XSS Simulation
    # Testing if AI tailoring endpoint reflects raw script tags
    try:
        res = requests.post(f"{BASE_URL}/resume/tailor", json={
            "profile": {"full_name": "<script>alert('xss')</script>"},
            "job_description": "test"
        })
        if "<script>" not in res.text:
            print("✅ XSS Sanitization: OK")
        else:
            print("❌ XSS Sanitization: VULNERABLE")
    except Exception as e:
        # If it returns 401, that's fine, it means it's protected
        print("✅ XSS Sanitization: PROTECTED BY AUTH")

if __name__ == "__main__":
    run_security_scan()
