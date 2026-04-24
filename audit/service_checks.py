import requests

def run_service_checks():
    print("\n⚙️ INFRASTRUCTURE & UPTIME CHECKS")

    services = {
        "API (FastAPI)": "http://localhost:8000/docs",
        "Frontend (Next.js)": "http://localhost:3000",
        "Analytics Dashboard": "http://localhost:3000/dashboard",
        "Monitoring (Grafana)": "http://localhost:3001"
    }

    for name, url in services.items():
        try:
            res = requests.get(url, timeout=5)
            if res.status_code < 400:
                print(f"✅ {name}: UP ({res.status_code})")
            else:
                print(f"⚠️ {name}: DEGRADED ({res.status_code})")
        except Exception:
            print(f"❌ {name}: DOWN")

if __name__ == "__main__":
    run_service_checks()
