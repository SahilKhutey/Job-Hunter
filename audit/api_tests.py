import requests

BASE_URL = "http://localhost:8000/api/v1"

def run_api_tests():
    print("\n🔍 API HEALTH & INTEGRITY TESTS")
    
    # 1. Health Check
    try:
        res = requests.get(f"{BASE_URL}/jobs") # Using an existing public/semi-public endpoint
        assert res.status_code in [200, 401] # 401 is fine as it confirms API is alive and protecting
        print("✅ API Reachability: OK")
    except Exception as e:
        print(f"❌ API Reachability: FAILED ({e})")

    # 2. Protected Route Isolation
    try:
        res = requests.get(f"{BASE_URL}/analytics/dashboard")
        if res.status_code == 401:
            print("✅ Route Protection (401): OK")
        else:
            print(f"❌ Route Protection: FAILED (Got {res.status_code})")
    except Exception as e:
        print(f"❌ Route Protection: ERROR ({e})")

if __name__ == "__main__":
    run_api_tests()
