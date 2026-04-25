import requests
import sys
import time

SERVICES = {
    "API": "http://localhost:8000/",
    "Frontend": "http://localhost:3000",
    "Dashboard Stats": "http://localhost:8000/api/v1/dashboard/stats",
}


def verify():
    print("--- Initializing HunterOS Deployment Verification ---")
    all_ok = True
    
    # 1. Basic Reachability
    for name, url in SERVICES.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 400:
                print(f"OK: {name}: Reachable ({response.status_code})")
            else:
                print(f"FAILED: {name}: Error ({response.status_code})")
                all_ok = False
        except Exception as e:
            print(f"FAILED: {name}: Unreachable ({str(e)})")
            all_ok = False

    # 2. Deep Health Check
    print("\n--- Running Deep Subsystem Audit ---")
    try:
        res = requests.get("http://localhost:8000/api/v1/health", timeout=10)
        data = res.json()
        print(f"System Status: {data['status']}")
        for sub, stat in data['details'].items():
            icon = "✅" if stat == "online" else "❌"
            print(f"  {icon} {sub.capitalize()}: {stat}")
            if stat != "online":
                all_ok = False
    except Exception as e:
        print(f"❌ Subsystem Audit Failed: {str(e)}")
        all_ok = False
            
    if all_ok:
        print("\nSYSTEM STATUS: ALL CLEAR. Deployment verified.")
    else:
        print("\nSYSTEM STATUS: DEGRADED. Check logs immediately.")
        sys.exit(1)


if __name__ == "__main__":
    verify()
