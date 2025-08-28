"""System mode implementations."""

from .core import SystemMode
from typing import Dict

class GamingMode(SystemMode):
    name = "gaming"
    description = "Gaming mode"
    
    def enable(self) -> bool:
        return True
    
    def disable(self) -> bool:
        return True
    
    def get_status(self) -> Dict[str, str]:
        return {"name": self.name, "active": "False"}

class AIMode(SystemMode):
    name = "ai"
    description = "AI mode"
    
    def enable(self) -> bool:
        return True
    
    def disable(self) -> bool:
        return True
    
    def get_status(self) -> Dict[str, str]:
        return {"name": self.name, "active": "False"}

class BalancedMode(SystemMode):
    name = "balanced"
    description = "Balanced mode"
    
    def enable(self) -> bool:
        return True
    
    def disable(self) -> bool:
        return True
    
    def get_status(self) -> Dict[str, str]:
        return {"name": self.name, "active": "False"}
