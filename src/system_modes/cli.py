"""
Command-line interface for system-modes package.
"""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from .core import SystemModeManager
from .modes import GamingMode, AIMode, BalancedMode

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """System Modes - Switch between gaming, AI, and balanced system modes."""
    pass


@main.command()
@click.option("--mode", "-m", type=click.Choice(["gaming", "ai", "balanced"]), 
              help="Mode to switch to")
@click.option("--list", "-l", is_flag=True, help="List available modes")
@click.option("--status", "-s", is_flag=True, help="Show current system status")
def switch(mode: Optional[str], list: bool, status: bool):
    """Switch system mode or show information."""
    manager = SystemModeManager()
    
    # Register all modes
    manager.register_mode(GamingMode())
    manager.register_mode(AIMode())
    manager.register_mode(BalancedMode())
    
    if list:
        _show_modes(manager)
    elif status:
        _show_status(manager)
    elif mode:
        _switch_mode(manager, mode)
    else:
        # Show current mode if no options specified
        current = manager.get_current_mode()
        if current:
            console.print(f"🎯 Current mode: [green]{current}[/green]")
        else:
            console.print("🎯 No mode currently active (using system defaults)")
        _show_modes(manager)


@main.command()
def modes():
    """List all available system modes."""
    manager = SystemModeManager()
    manager.register_mode(GamingMode())
    manager.register_mode(AIMode())
    manager.register_mode(BalancedMode())
    _show_modes(manager)


@main.command()
def status():
    """Show current system status."""
    manager = SystemModeManager()
    manager.register_mode(GamingMode())
    manager.register_mode(AIMode())
    manager.register_mode(BalancedMode())
    _show_status(manager)


@main.command()
@click.argument("mode", type=click.Choice(["gaming", "ai", "balanced"]))
def enable(mode: str):
    """Enable a specific system mode."""
    manager = SystemModeManager()
    manager.register_mode(GamingMode())
    manager.register_mode(AIMode())
    manager.register_mode(BalancedMode())
    _switch_mode(manager, mode)


@main.command()
def disable():
    """Disable current mode and return to balanced."""
    manager = SystemModeManager()
    manager.register_mode(GamingMode())
    manager.register_mode(AIMode())
    manager.register_mode(BalancedMode())
    
    current = manager.get_current_mode()
    if current and current != "balanced":
        console.print(f"🔄 Disabling {current} mode...")
        manager.switch_to_mode("balanced")
        console.print("✅ Returned to balanced mode")
    else:
        console.print("ℹ️  Already in balanced mode")


def _show_modes(manager: SystemModeManager):
    """Display available modes in a nice table."""
    table = Table(title="🎯 Available System Modes")
    table.add_column("Mode", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Status", style="green")
    
    current_mode = manager.get_current_mode()
    
    for name, mode in manager.modes.items():
        status = "🟢 Active" if name == current_mode else "⚪ Inactive"
        table.add_row(name.title(), mode.description, status)
    
    console.print(table)


def _show_status(manager: SystemModeManager):
    """Display system status in a nice table."""
    status = manager.get_system_status()
    
    table = Table(title="📊 System Status")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    
    for key, value in status.items():
        key_display = key.replace("_", " ").title()
        table.add_row(key_display, str(value))
    
    console.print(table)
    
    # Show GPU information
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name,utilization.gpu,memory.used,memory.total", 
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, check=True
        )
        
        gpu_table = Table(title="🎮 GPU Status")
        gpu_table.add_column("GPU", style="cyan")
        gpu_table.add_column("Name", style="white")
        gpu_table.add_column("Utilization", style="green")
        gpu_table.add_column("Memory", style="yellow")
        
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(', ')
                gpu_table.add_row(parts[0], parts[1], f"{parts[2]}%", f"{parts[3]}MB/{parts[4]}MB")
        
        console.print(gpu_table)
    except Exception:
        console.print("⚠️  Could not retrieve GPU information")


def _switch_mode(manager: SystemModeManager, mode: str):
    """Switch to the specified mode."""
    success = manager.switch_to_mode(mode)
    if success:
        console.print(f"✅ Successfully switched to [green]{mode}[/green] mode")
        
        # Show what this mode is optimized for
        mode_info = {
            "gaming": "🎮 Optimized for maximum gaming performance with RTX 4060 Ti",
            "ai": "🤖 Optimized for AI development and CUDA workloads with RTX 4060 Ti",
            "balanced": "⚖️ Standard Ubuntu settings for balanced performance and power"
        }
        console.print(f"💡 {mode_info.get(mode, '')}")
    else:
        console.print(f"❌ Failed to switch to {mode} mode")
        sys.exit(1)


if __name__ == "__main__":
    main()
