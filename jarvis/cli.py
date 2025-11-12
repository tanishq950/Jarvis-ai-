"""
Command-line interface for Jarvis AI
"""
import click
import asyncio
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from jarvis.core.orchestrator import Orchestrator
from jarvis.core.config import settings
from jarvis.core.logger import logger
from jarvis.ui.api import run_server


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Jarvis AI - Your comprehensive AI assistant
    
    A modular AI system for automation, security, development, and learning.
    """
    pass


@cli.command()
@click.option("--host", default=None, help="Server host")
@click.option("--port", default=None, type=int, help="Server port")
def serve(host: Optional[str], port: Optional[int]):
    """Start the Jarvis AI API server"""
    click.echo("🤖 Starting Jarvis AI server...")
    run_server(host, port)


@cli.command()
@click.option("--live", is_flag=True, help="Enable live mode (executes immediately)")
@click.option("--safe", is_flag=True, help="Enable safe mode (maximum confirmations)")
@click.option("--teach", is_flag=True, help="Enable teaching mode (explains everything)")
@click.option("--auto-repair", is_flag=True, help="Enable auto-repair (fixes issues automatically)")
def chat(live: bool, safe: bool, teach: bool, auto_repair: bool):
    """Start interactive chat mode"""
    click.echo("🤖 Jarvis AI - Interactive Chat")
    click.echo("=" * 50)
    
    # Initialize orchestrator
    orchestrator = Orchestrator()
    
    # Set execution mode
    if live:
        click.echo("⚠️  WARNING: Live mode enabled!")
        click.echo("Commands will execute with minimal confirmation.")
        confirm = click.confirm("Are you sure you want to enable live mode?", default=False)
        if confirm:
            asyncio.run(orchestrator.start())
            orchestrator.enable_live_mode(confirm=True)
        else:
            click.echo("Live mode not enabled. Using normal mode.")
            asyncio.run(orchestrator.start())
    elif safe:
        click.echo("🔒 Safe mode enabled - maximum safety checks")
        asyncio.run(orchestrator.start())
        orchestrator.set_execution_mode("safe")
    else:
        asyncio.run(orchestrator.start())
    
    # Enable teaching mode if requested
    if teach:
        click.echo("🎓 Teaching mode enabled - I'll explain everything!")
        orchestrator.enable_teaching_mode()
    
    # Enable auto-repair if requested
    if auto_repair:
        click.echo("🔧 Auto-repair mode enabled!")
        confirm = click.confirm("Auto-repair will modify your system. Continue?", default=False)
        if confirm:
            orchestrator.enable_auto_repair(confirm=True)
            click.echo("✓ Auto-repair enabled - System will fix issues automatically")
        else:
            click.echo("Auto-repair not enabled")
    
    click.echo("\nType 'help' for commands, 'exit' to quit")
    click.echo("=" * 50 + "\n")
    
    # Interactive loop
    while True:
        try:
            user_input = click.prompt("You", type=str, prompt_suffix=" > ")
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                click.echo("Goodbye! 👋")
                asyncio.run(orchestrator.stop())
                break
            
            elif user_input.lower() == "help":
                show_help()
                continue
            
            elif user_input.lower() == "status":
                status = orchestrator.get_status()
                health = orchestrator.get_system_health()
                click.echo(f"\nSystem Status:")
                click.echo(f"  Running: {status['running']}")
                click.echo(f"  Mode: {status['execution_mode']}")
                click.echo(f"  Live Mode: {status['live_mode_enabled']}")
                click.echo(f"  Teaching Mode: {status['teaching_mode_enabled']}")
                click.echo(f"  Auto-Repair: {status['auto_repair_enabled']}")
                click.echo(f"  Health: {health['status']}")
                click.echo(f"  Agents: {', '.join(status['agents'])}")
                click.echo(f"  Plugins: {', '.join(status['plugins'])}")
                click.echo()
                continue
            
            elif user_input.lower() in ["diagnose", "diagnostics", "health check"]:
                diagnostics = orchestrator.get_diagnostics()
                click.echo(f"\nSystem Diagnostics:")
                click.echo(f"  Auto-Repair: {'Enabled' if diagnostics['auto_repair_enabled'] else 'Disabled'}")
                click.echo(f"  Issues Detected: {diagnostics['total_issues_detected']}")
                click.echo(f"  Unresolved: {diagnostics['unresolved_issues']}")
                click.echo(f"  Repair Attempts: {diagnostics['repair_attempts']}")
                
                if diagnostics['recent_issues']:
                    click.echo(f"\n  Recent Issues:")
                    for issue in diagnostics['recent_issues'][-5:]:
                        status_icon = "✓" if issue['resolved'] else "✗"
                        click.echo(f"    {status_icon} [{issue['severity']}] {issue['description']}")
                
                click.echo()
                continue
            
            elif user_input.lower() in ["enable auto repair", "enable auto-repair", "auto repair"]:
                confirm = click.confirm("⚠️  Enable auto-repair? System will fix issues automatically!", default=False)
                result = orchestrator.enable_auto_repair(confirm=confirm)
                click.echo(f"Jarvis: {result.get('message')}")
                if result.get('warning'):
                    click.echo(f"⚠️  {result['warning']}")
                continue
            
            elif user_input.lower() in ["disable auto repair", "disable auto-repair", "stop auto repair"]:
                result = orchestrator.disable_auto_repair()
                click.echo(f"Jarvis: {result.get('message')}")
                continue
            
            elif user_input.lower() in ["teach me", "enable teaching", "teaching mode"]:
                result = orchestrator.enable_teaching_mode()
                click.echo(f"Jarvis: {result.get('message')}")
                if result.get('features'):
                    click.echo("\nTeaching mode features:")
                    for feature in result['features']:
                        click.echo(f"  • {feature}")
                click.echo()
                continue
            
            elif user_input.lower() in ["stop teaching", "disable teaching"]:
                result = orchestrator.disable_teaching_mode()
                click.echo(f"Jarvis: {result.get('message')}")
                continue
            
            elif user_input.lower() == "enable live mode":
                confirm = click.confirm("⚠️  Enable live mode? Commands will execute immediately!", default=False)
                result = orchestrator.enable_live_mode(confirm=confirm)
                click.echo(f"Jarvis: {result.get('message')}")
                if result.get('warning'):
                    click.echo(f"⚠️  {result['warning']}")
                continue
            
            elif user_input.lower() == "disable live mode":
                result = orchestrator.disable_live_mode()
                click.echo(f"Jarvis: {result.get('message')}")
                continue
            
            # Process command
            result = asyncio.run(orchestrator.process_command(user_input))
            
            # Display result
            if result.get("success"):
                click.echo(f"Jarvis: {result.get('message', 'Task completed')}")
                
                # Show additional info if available
                if "explanation" in result:
                    click.echo(f"\n{result['explanation']}")
                
                if "code" in result:
                    click.echo(f"\nGenerated code:")
                    click.echo("```")
                    click.echo(result['code'])
                    click.echo("```")
                
                if "results" in result:
                    click.echo(f"\nResults: {result['results']}")
            else:
                if result.get("requires_approval"):
                    click.echo("⚠️  This action requires approval:")
                    click.echo(f"   {result.get('message')}")
                    if click.confirm("Approve?", default=False):
                        # Re-execute with approval
                        result = asyncio.run(
                            orchestrator.process_command(user_input, user_approved=True)
                        )
                        click.echo(f"Jarvis: {result.get('message', 'Task completed')}")
                elif result.get("issue_detected"):
                    # Show diagnostic information
                    issue = result["issue_detected"]
                    click.echo(f"❌ Error: {result.get('error')}")
                    click.echo(f"\n🔍 Issue Detected:")
                    click.echo(f"   Type: {issue['type']}")
                    click.echo(f"   Severity: {issue['severity']}")
                    click.echo(f"   Description: {issue['description']}")
                    
                    if result.get('suggested_fixes'):
                        click.echo(f"\n💡 Suggested Fixes:")
                        for fix in result['suggested_fixes']:
                            click.echo(f"   • {fix}")
                    
                    if result.get('auto_repair_available'):
                        click.echo(f"\n💡 Tip: Enable auto-repair to fix issues automatically")
                        click.echo(f"   Command: enable auto repair")
                else:
                    click.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            click.echo()  # Empty line for readability
            
        except KeyboardInterrupt:
            click.echo("\n\nInterrupted. Type 'exit' to quit.")
            continue
        except Exception as e:
            click.echo(f"❌ Error: {e}")
            logger.error(f"Chat error: {e}", exc_info=True)


def show_help():
    """Display help information"""
    help_text = """
Available Commands:
  help               - Show this help message
  status             - Show system status
  diagnostics        - Show detailed diagnostics
  enable live mode   - Enable live execution mode
  disable live mode  - Disable live execution mode
  teach me           - Enable teaching mode (explains everything)
  stop teaching      - Disable teaching mode
  enable auto repair - Enable automatic repair system
  disable auto repair- Disable automatic repair system
  exit/quit          - Exit the chat

Modes:
  Live Mode:
    Commands execute immediately with minimal confirmation.
    Use with caution!

  Teaching Mode:
    Explains every command and tool in detail.
    Perfect for learning Kali Linux tools and security concepts!

  Auto-Repair Mode:
    Automatically detects and fixes common issues:
    • Missing dependencies (pip install)
    • Missing tools (apt install)
    • Configuration errors
    • And more!

Kali Linux Tools:
  You can use any Kali tool! Examples:
  "nmap -sV target.com"
  "explain metasploit"
  "run nikto on target.com"
  "teach me about hydra"

Examples:
  "Explain what pentesting is"
  "Generate a Python script to list files"
  "Monitor system security"
  "Scan target.com" (requires authorization)
  "Teach me how to use nmap"
  "Diagnose system issues"
"""
    click.echo(help_text)


@cli.command()
def agents():
    """List all available agents"""
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())
    
    agent_list = orchestrator.agent_manager.list_agents()
    capabilities = orchestrator.agent_manager.get_capabilities()
    
    click.echo("Available Agents:")
    click.echo("=" * 50)
    
    for agent_name in agent_list:
        caps = capabilities.get(agent_name, [])
        click.echo(f"\n{agent_name}:")
        for cap in caps:
            click.echo(f"  - {cap}")
    
    asyncio.run(orchestrator.stop())


@cli.command()
def status():
    """Show system status"""
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())
    
    status = orchestrator.get_status()
    
    click.echo("Jarvis AI System Status")
    click.echo("=" * 50)
    click.echo(f"Running: {status['running']}")
    click.echo(f"Execution Mode: {status['execution_mode']}")
    click.echo(f"Live Mode: {status['live_mode_enabled']}")
    click.echo(f"\nAgents ({len(status['agents'])}):")
    for agent in status['agents']:
        click.echo(f"  - {agent}")
    click.echo(f"\nPlugins ({len(status['plugins'])}):")
    for plugin in status['plugins']:
        click.echo(f"  - {plugin}")
    
    asyncio.run(orchestrator.stop())


@cli.command()
@click.argument("command")
@click.option("--live", is_flag=True, help="Execute in live mode")
def execute(command: str, live: bool):
    """Execute a single command"""
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())
    
    if live:
        orchestrator.enable_live_mode(confirm=True)
    
    result = asyncio.run(orchestrator.process_command(command))
    
    if result.get("success"):
        click.echo(f"✓ {result.get('message', 'Success')}")
        if result.get("code"):
            click.echo(result["code"])
    else:
        click.echo(f"✗ {result.get('error', 'Failed')}")
    
    asyncio.run(orchestrator.stop())


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
