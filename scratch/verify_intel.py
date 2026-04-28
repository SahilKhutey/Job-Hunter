import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.intelligence_engine import UserIntelligenceEngine

async def verify_intelligence():
    engine = UserIntelligenceEngine()
    
    test_cases = [
        {
            "name": "Burnout",
            "jd": "24/7 availability and work hard play hard culture."
        },
        {
            "name": "Instability",
            "jd": "Immediate hire for vacancy backfill."
        },
        {
            "name": "Ambiguity",
            "jd": "Wear many hats and handle various tasks as needed."
        },
        {
            "name": "Combined High Risk",
            "jd": "Rockstars for 24/7 startup. Urgent backfill. Competitive pay for wearing many hats."
        }
    ]
    
    print("\n--- NEURAL INTELLIGENCE VERIFICATION ---")
    for case in test_cases:
        # analyze_red_flags is synchronous
        analysis = engine.analyze_red_flags(case["jd"])
        print(f"\n[CASE: {case['name']}]")
        print(f"Flags Detected: {analysis['flags']}")
        print(f"Risk Score: {analysis['risk_score']}")
        
        # Validation
        if case["name"] == "Combined High Risk":
            assert analysis["risk_score"] >= 75
        else:
            assert len(analysis["flags"]) >= 1
            assert analysis["risk_score"] >= 25
            
    print("\n[SUCCESS] Intelligence Logic Verified.")

if __name__ == "__main__":
    asyncio.run(verify_intelligence())
