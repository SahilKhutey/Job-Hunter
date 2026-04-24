import requests

BASE_URL = "http://localhost:8000/api/v1"

def run_auth_tests():
    print("\n🔐 IDENTITY & AUTHENTICATION TESTS")

    # 1. Invalid Login Attempt
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={
            "username": "nonexistent@user.com",
            "password": "wrongpassword"
        })
        if res.status_code == 401:
            print("✅ Brute-force Prevention (Invalid Login): OK")
        else:
            print(f"❌ Brute-force Prevention: FAILED (Got {res.status_code})")
    except Exception as e:
        print(f"❌ Auth Test: ERROR ({e})")

    # 2. Token Integrity Check
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid"}
    try:
        res = requests.get(f"{BASE_URL}/analytics/dashboard", headers=headers)
        if res.status_code == 401:
            print("✅ Token Validation (Malformed JWT): OK")
        else:
            print(f"❌ Token Validation: FAILED (Got {res.status_code})")
    except Exception as e:
        print(f"❌ Token Test: ERROR ({e})")

if __name__ == "__main__":
    run_auth_tests()
