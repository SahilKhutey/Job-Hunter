from typing import Dict, Any

class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes the current state, performs agent-specific logic, 
        and returns the mutated/updated state.
        """
        raise NotImplementedError("Each agent must implement its own run() method.")
