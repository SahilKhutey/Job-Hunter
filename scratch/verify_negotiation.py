import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.negotiation_service import NegotiationService

async def verify_negotiation():
    service = NegotiationService()
    
    # Mock data
    offer = {"base_salary": "$120,000", "equity": "0.1%", "bonus": "$10,000"}
    job_details = {
        "title": "Senior AI Engineer",
        "company": "DeepMind",
        "strategic_risk_score": 45,
        "red_flags": ["High-paced environment"]
    }
    
    # Test Roleplay Simulation
    history = [
        {"role": "user", "content": "I appreciate the offer, but given my 10 years of experience in LLMs, I was expecting a base closer to $150,000."}
    ]
    
    print("\n--- NEGOTIATION ROLEPLAY VERIFICATION ---")
    
    # simulate_roleplay is async
    result = await service.simulate_roleplay(history, offer, job_details)
    
    print(f"\n[HM RESPONSE]: {result['response']}")
    print(f"[METRICS]: {result['metrics']}")
    
    assert "response" in result
    assert "metrics" in result
    assert 0 <= result['metrics']['leverage_impact'] <= 100
    
    # Test Leverage Impact Logic (Mocking the second turn)
    history.append({"role": "assistant", "content": result['response']})
    history.append({"role": "user", "content": "I understand the budget constraints, but can we look at increasing the equity stake or adding a sign-on bonus to bridge the gap?"})
    
    result_turn_2 = await service.simulate_roleplay(history, offer, job_details)
    print(f"\n[TURN 2 RESPONSE]: {result_turn_2['response']}")
    print(f"[TURN 2 METRICS]: {result_turn_2['metrics']}")
    
    print("\n[SUCCESS] Negotiation Simulation Logic Verified.")

if __name__ == "__main__":
    asyncio.run(verify_negotiation())
