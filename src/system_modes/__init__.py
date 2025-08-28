"""
System Modes - A Python package for switching between gaming, AI, and balanced system modes.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import SystemModeManager
from .modes import GamingMode, AIMode, BalancedMode

__all__ = [
    "SystemModeManager",
    "GamingMode", 
    "AIMode",
    "BalancedMode",
]
