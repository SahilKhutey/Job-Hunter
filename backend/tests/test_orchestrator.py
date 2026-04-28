import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.agents.orchestrator import Orchestrator
from app.agents.base_agent import BaseAgent

class MockAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.run = AsyncMock()

@pytest.mark.asyncio
async def test_orchestrator_parallel_execution():
    agent1 = MockAgent("agent1")
    agent2 = MockAgent("agent2")
    
    agent1.run.return_value = {"key1": "val1"}
    agent2.run.return_value = {"key2": "val2"}
    
    orchestrator = Orchestrator(stages=[[agent1, agent2]])
    state = {"initial": "state"}
    
    new_state = await orchestrator.run(state)
    
    assert new_state["key1"] == "val1"
    assert new_state["key2"] == "val2"
    assert agent1.run.called
    assert agent2.run.called

@pytest.mark.asyncio
async def test_orchestrator_skipping_logic():
    agent_exec = MockAgent("execution")
    
    orchestrator = Orchestrator(stages=[[agent_exec]])
    state = {"match_score": 0.4} # Low score
    
    new_state = await orchestrator.run(state)
    
    assert not agent_exec.run.called
    assert "error" not in new_state

@pytest.mark.asyncio
async def test_orchestrator_error_halting():
    agent1 = MockAgent("agent1")
    agent2 = MockAgent("agent2")
    
    agent1.run.side_effect = Exception("Stage 1 Failed")
    
    orchestrator = Orchestrator(stages=[[agent1], [agent2]])
    state = {}
    
    new_state = await orchestrator.run(state)
    
    assert new_state["error"] == "Stage 1 Failed"
    assert not agent2.run.called
