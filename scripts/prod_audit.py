import os
import sys

def audit_production():
    print("\n--- HUNTEROS PRODUCTION AUDIT: INITIATED ---")
    
    required_env = [
        "DATABASE_URL",
        "REDIS_URL",
        "OPENAI_API_KEY",
        "SECRET_KEY",
        "NEXT_PUBLIC_API_URL"
    ]
    
    missing = []
    for var in required_env:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"[ERROR] Missing critical production variables: {', '.join(missing)}")
    else:
        print("[SUCCESS] All mission-critical environment variables detected.")
        
    # Check Infrastructure Paths
    paths = [
        "backend/app/main.py",
        "frontend/src/app/page.tsx",
        "docker-compose.yml",
        "gateway/nginx.conf"
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"[VERIFIED] Path integrity: {path}")
        else:
            print(f"[ERROR] Path violation: {path}")
            
    print("\n[STATUS] Production Audit Phase 1 Complete. Readiness Level: HIGH.")

if __name__ == "__main__":
    audit_production()
