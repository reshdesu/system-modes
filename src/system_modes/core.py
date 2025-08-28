"""
Core system mode management functionality.
"""

import os
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import psutil


class SystemMode(ABC):
    """Abstract base class for system modes."""
    
    name: str
    description: str
    
    @abstractmethod
    def enable(self) -> bool:
        """Enable this system mode."""
        pass
    
    @abstractmethod
    def disable(self) -> bool:
        """Disable this system mode."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, str]:
        """Get current status of this mode."""
        pass


class SystemModeManager:
    """Manages system mode switching between gaming, AI, and balanced modes."""
    
    def __init__(self):
        self.modes: Dict[str, SystemMode] = {}
        self.current_mode: Optional[str] = None
        self._check_root()
    
    def _check_root(self) -> None:
        """Check if running with root privileges."""
        if os.geteuid() != 0:
            print("⚠️  Warning: Some operations require root privileges")
            print("   Run with 'sudo' for full functionality")
    
    def register_mode(self, mode: SystemMode) -> None:
        """Register a new system mode."""
        self.modes[mode.name] = mode
    
    def get_available_modes(self) -> List[str]:
        """Get list of available mode names."""
        return list(self.modes.keys())
    
    def switch_to_mode(self, mode_name: str) -> bool:
        """Switch to the specified system mode."""
        if mode_name not in self.modes:
            print(f"❌ Mode '{mode_name}' not found")
            return False
        
        print(f"🔄 Switching to {mode_name} mode...")
        
        # Disable current mode if any
        if self.current_mode and self.current_mode in self.modes:
            self.modes[self.current_mode].disable()
        
        # Enable new mode
        success = self.modes[mode_name].enable()
        if success:
            self.current_mode = mode_name
            print(f"✅ Successfully switched to {mode_name} mode")
        else:
            print(f"❌ Failed to switch to {mode_name} mode")
        
        return success
    
    def get_current_mode(self) -> Optional[str]:
        """Get the name of the currently active mode."""
        return self.current_mode
    
    def get_system_status(self) -> Dict[str, str]:
        """Get overall system status."""
        status = {
            "cpu_governor": self._get_cpu_governor(),
            "gpu_persistence": self._get_gpu_persistence(),
            "memory_swappiness": self._get_memory_swappiness(),
            "current_mode": self.current_mode or "Unknown",
        }
        return status
    
    def _get_cpu_governor(self) -> str:
        """Get current CPU governor."""
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as f:
                return f.read().strip()
        except (FileNotFoundError, PermissionError):
            return "Unknown"
    
    def _get_gpu_persistence(self) -> str:
        """Get GPU persistence mode."""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=persistence_mode", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip().split(",")[0]
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "Unknown"
    
    def _get_memory_swappiness(self) -> str:
        """Get memory swappiness value."""
        try:
            with open("/proc/sys/vm/swappiness", "r") as f:
                return f.read().strip()
        except (FileNotFoundError, PermissionError):
            return "Unknown"
    
    def list_modes(self) -> None:
        """List all available modes with descriptions."""
        print("🎯 Available System Modes:")
        print("==========================")
        for name, mode in self.modes.items():
            current = " (Current)" if name == self.current_mode else ""
            print(f"  {name}{current}: {mode.description}")
        print()
    
    def show_status(self) -> None:
        """Show current system status."""
        status = self.get_system_status()
        print("📊 System Status:")
        print("=================")
        for key, value in status.items():
            key_display = key.replace("_", " ").title()
            print(f"  {key_display}: {value}")
        print()
