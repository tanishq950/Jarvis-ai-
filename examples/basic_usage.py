#!/usr/bin/env python3
"""
Example: Using Jarvis AI Programmatically

This script demonstrates how to use Jarvis AI in your own Python code.
"""
import asyncio
from jarvis.core.orchestrator import Orchestrator


async def main():
    """Main example function"""
    
    # Initialize Jarvis
    print("🤖 Initializing Jarvis AI...")
    jarvis = Orchestrator()
    await jarvis.start()
    
    # Enable teaching mode for learning
    print("\n🎓 Enabling teaching mode...")
    result = jarvis.enable_teaching_mode()
    print(f"   {result['message']}")
    
    # Example 1: Ask for explanation
    print("\n" + "="*50)
    print("Example 1: Learning about tools")
    print("="*50)
    
    command = "explain what nmap does"
    print(f"\nCommand: {command}")
    result = await jarvis.process_command(command)
    
    if result.get('success'):
        print(f"\n✓ Success!")
        if 'explanation' in result:
            print(f"\nExplanation: {result['explanation']}")
    
    # Example 2: Generate code
    print("\n" + "="*50)
    print("Example 2: Code generation")
    print("="*50)
    
    command = "generate a Python script to list files"
    print(f"\nCommand: {command}")
    result = await jarvis.process_command(command)
    
    if result.get('success'):
        print(f"\n✓ Success!")
        if 'code' in result:
            print(f"\nGenerated code:\n{result['code']}")
    
    # Example 3: System status
    print("\n" + "="*50)
    print("Example 3: System status")
    print("="*50)
    
    status = jarvis.get_status()
    print(f"\nSystem Status:")
    print(f"  Running: {status['running']}")
    print(f"  Mode: {status['execution_mode']}")
    print(f"  Teaching: {status['teaching_mode_enabled']}")
    print(f"  Health: {status['health_status']}")
    print(f"  Agents: {', '.join(status['agents'])}")
    
    # Example 4: Diagnostics
    print("\n" + "="*50)
    print("Example 4: System diagnostics")
    print("="*50)
    
    diagnostics = jarvis.get_diagnostics()
    print(f"\nDiagnostics:")
    print(f"  Auto-Repair: {diagnostics['auto_repair_enabled']}")
    print(f"  Issues Detected: {diagnostics['total_issues_detected']}")
    print(f"  Unresolved: {diagnostics['unresolved_issues']}")
    
    # Clean shutdown
    print("\n🛑 Shutting down...")
    await jarvis.stop()
    print("✓ Done!")


if __name__ == "__main__":
    asyncio.run(main())
