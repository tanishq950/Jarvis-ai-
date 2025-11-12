"""
Core Orchestrator - Main Jarvis AI system coordinator
"""
from typing import Dict, Any, Optional
import asyncio
from pathlib import Path

from .config import settings
from .logger import logger, audit_logger
from .policy_engine import PolicyEngine
from .memory import MemoryManager
from .agent_manager import AgentManager
from .auto_repair import AutoRepairSystem
from ..plugins.plugin_manager import PluginManager


class ExecutionMode:
    """Execution mode configuration"""
    SAFE = "safe"  # Requires confirmation for everything
    NORMAL = "normal"  # Policy-based confirmations
    LIVE = "live"  # Minimal confirmations, executes immediately


class Orchestrator:
    """
    Main orchestrator for Jarvis AI system.
    Coordinates all components: agents, plugins, memory, and policy enforcement.
    """
    
    def __init__(self):
        logger.info("Initializing Jarvis AI Orchestrator...")
        
        # Initialize core components
        self.policy_engine = PolicyEngine(settings.policy_file)
        self.memory = MemoryManager(settings.memory_db_path)
        self.agent_manager = AgentManager(self.policy_engine)
        self.plugin_manager = PluginManager(self.policy_engine)
        self.auto_repair = AutoRepairSystem(self.policy_engine)
        
        # Execution mode
        self.execution_mode = ExecutionMode.NORMAL
        self.live_mode_enabled = False
        self.teaching_mode_enabled = False
        self.auto_repair_enabled = False
        
        # System state
        self.running = False
        self.session_id = None
        
        logger.info("Jarvis AI Orchestrator initialized successfully")
    
    async def start(self):
        """Start the orchestrator"""
        if self.running:
            logger.warning("Orchestrator already running")
            return
        
        self.running = True
        logger.info("Jarvis AI system started")
        audit_logger.log_action(
            action="system.start",
            resource="orchestrator",
            result="success"
        )
    
    async def stop(self):
        """Stop the orchestrator"""
        if not self.running:
            return
        
        logger.info("Stopping Jarvis AI system...")
        self.running = False
        
        audit_logger.log_action(
            action="system.stop",
            resource="orchestrator",
            result="success"
        )
    
    def enable_live_mode(self, confirm: bool = False):
        """
        Enable live mode for immediate execution.
        
        Args:
            confirm: User must explicitly confirm to enable live mode
        """
        if not confirm:
            logger.warning("Live mode requires explicit confirmation")
            return {
                "success": False,
                "message": "Live mode is dangerous. Set confirm=True to enable.",
                "warning": "Live mode will execute commands with minimal confirmation!"
            }
        
        self.live_mode_enabled = True
        self.execution_mode = ExecutionMode.LIVE
        
        logger.warning("⚠️  LIVE MODE ENABLED - Commands will execute immediately!")
        audit_logger.log_action(
            action="system.enable_live_mode",
            resource="orchestrator",
            result="enabled",
            metadata={"execution_mode": self.execution_mode}
        )
        
        return {
            "success": True,
            "message": "Live mode enabled. Commands will execute with minimal confirmation.",
            "warning": "Use caution - this bypasses many safety checks!"
        }
    
    def disable_live_mode(self):
        """Disable live mode and return to normal mode"""
        self.live_mode_enabled = False
        self.execution_mode = ExecutionMode.NORMAL
        
        logger.info("Live mode disabled, returning to normal mode")
        audit_logger.log_action(
            action="system.disable_live_mode",
            resource="orchestrator",
            result="disabled"
        )
        
        return {
            "success": True,
            "message": "Live mode disabled. Normal safety checks restored."
        }
    
    def set_execution_mode(self, mode: str):
        """
        Set execution mode.
        
        Args:
            mode: One of 'safe', 'normal', 'live'
        """
        valid_modes = [ExecutionMode.SAFE, ExecutionMode.NORMAL, ExecutionMode.LIVE]
        
        if mode not in valid_modes:
            return {
                "success": False,
                "error": f"Invalid mode. Choose from: {valid_modes}"
            }
        
        self.execution_mode = mode
        self.live_mode_enabled = (mode == ExecutionMode.LIVE)
        
        logger.info(f"Execution mode set to: {mode}")
        
        return {
            "success": True,
            "mode": mode,
            "message": f"Execution mode set to {mode}"
        }
    
    def enable_teaching_mode(self):
        """Enable teaching mode - system explains everything"""
        self.teaching_mode_enabled = True
        result = self.plugin_manager.enable_teaching_mode()
        
        logger.info("🎓 Teaching mode enabled")
        audit_logger.log_action(
            action="system.enable_teaching_mode",
            resource="orchestrator",
            result="enabled"
        )
        
        return {
            "success": True,
            "message": "Teaching mode enabled. I'll explain everything I do!",
            "features": [
                "Detailed explanations for every command",
                "Learning points and best practices",
                "Step-by-step guidance",
                "Security warnings and recommendations"
            ]
        }
    
    def disable_teaching_mode(self):
        """Disable teaching mode"""
        self.teaching_mode_enabled = False
        self.plugin_manager.disable_teaching_mode()
        
        logger.info("Teaching mode disabled")
        audit_logger.log_action(
            action="system.disable_teaching_mode",
            resource="orchestrator",
            result="disabled"
        )
        
        return {
            "success": True,
            "message": "Teaching mode disabled."
        }
    
    def enable_auto_repair(self, confirm: bool = False):
        """
        Enable automatic repair system.
        
        Args:
            confirm: User must explicitly confirm to enable auto-repair
        """
        result = self.auto_repair.enable_auto_repair(confirm=confirm)
        self.auto_repair_enabled = result.get("success", False)
        return result
    
    def disable_auto_repair(self):
        """Disable automatic repair system"""
        result = self.auto_repair.disable_auto_repair()
        self.auto_repair_enabled = False
        return result
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        return self.auto_repair.get_health_status()
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """Get detailed diagnostics"""
        return self.auto_repair.get_diagnostics()
    
    async def process_command(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None,
        user_approved: bool = False
    ) -> Dict[str, Any]:
        """
        Process a user command with error handling and auto-repair.
        
        Args:
            command: User command/query
            context: Additional context
            user_approved: Whether user has pre-approved this action
        
        Returns:
            Command execution results
        """
        context = context or {}
        context["execution_mode"] = self.execution_mode
        context["live_mode"] = self.live_mode_enabled
        context["user_approved"] = user_approved
        
        # Store in memory
        self.memory.short_term.add_message("user", command)
        
        logger.info(f"Processing command: {command}")
        
        # Parse intent (placeholder - would use LLM)
        intent = self._parse_intent(command)
        
        # Try to execute with error handling and auto-repair
        max_retries = 3 if self.auto_repair_enabled else 1
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Route to appropriate agent
                result = await self.agent_manager.execute_task(
                    task=command,
                    context=context
                )
                
                # Store result in memory
                self.memory.short_term.add_message("assistant", str(result))
                
                # Log event
                self.memory.long_term.log_event(
                    event_type="command_execution",
                    description=command,
                    metadata=result
                )
                
                return result
                
            except Exception as e:
                last_error = e
                logger.error(f"Command execution error (attempt {attempt + 1}/{max_retries}): {e}")
                
                # Diagnose the issue
                issue = self.auto_repair.diagnose(e, context={"command": command})
                
                # Attempt repair if enabled
                if self.auto_repair_enabled and attempt < max_retries - 1:
                    logger.info(f"Attempting auto-repair: {issue.description}")
                    repair_result = self.auto_repair.repair(issue, auto=True)
                    
                    if repair_result.get("success"):
                        logger.info("Auto-repair successful, retrying command...")
                        continue  # Retry the command
                    else:
                        logger.warning(f"Auto-repair failed: {repair_result.get('message')}")
                
                # If this is the last attempt or auto-repair is disabled, return error
                if attempt == max_retries - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "issue_detected": {
                            "type": issue.issue_type.value,
                            "description": issue.description,
                            "severity": issue.severity
                        },
                        "suggested_fixes": issue.suggested_fixes,
                        "auto_repair_available": not self.auto_repair_enabled,
                        "message": "Command failed. Enable auto-repair to attempt automatic fixes."
                    }
        
        # Should not reach here, but just in case
        return {
            "success": False,
            "error": str(last_error) if last_error else "Unknown error"
        }
    
    def _parse_intent(self, command: str) -> Dict[str, Any]:
        """
        Parse user intent from command.
        Placeholder for LLM-based intent recognition.
        """
        command_lower = command.lower()
        
        # Check for teaching mode
        if "teach me" in command_lower or "enable teaching" in command_lower or "teaching mode" in command_lower:
            return {
                "action": "enable_teaching_mode",
                "requires_confirmation": False
            }
        
        if "stop teaching" in command_lower or "disable teaching" in command_lower:
            return {
                "action": "disable_teaching_mode"
            }
        
        # Check for auto-repair
        if "enable auto repair" in command_lower or "auto repair" in command_lower or "enable auto-repair" in command_lower:
            return {
                "action": "enable_auto_repair",
                "requires_confirmation": True
            }
        
        if "disable auto repair" in command_lower or "stop auto repair" in command_lower:
            return {
                "action": "disable_auto_repair"
            }
        
        if "diagnose" in command_lower or "health check" in command_lower or "system health" in command_lower:
            return {
                "action": "get_diagnostics"
            }
        
        # Check for live mode activation
        if "enable live mode" in command_lower or "run live" in command_lower:
            return {
                "action": "enable_live_mode",
                "requires_confirmation": True
            }
        
        if "disable live mode" in command_lower or "stop live" in command_lower:
            return {
                "action": "disable_live_mode"
            }
        
        # Check for Kali tool usage
        kali_tools = ["nmap", "metasploit", "hydra", "sqlmap", "burp", "wireshark", 
                      "aircrack", "john", "hashcat", "nikto", "dirb", "gobuster"]
        
        for tool in kali_tools:
            if tool in command_lower:
                return {
                    "action": "use_tool",
                    "tool": tool,
                    "command": command
                }
        
        # Check for GitHub operations
        github_keywords = ["github", "repo", "repository", "project", "issue", "pull request", "pr"]
        github_actions = {
            "create repo": "create_repo",
            "make repo": "create_repo",
            "new repo": "create_repo",
            "create repository": "create_repo",
            "list repos": "list_repos",
            "show repos": "list_repos",
            "my repos": "list_repos",
            "clone": "clone_repo",
            "create issue": "create_issue",
            "new issue": "create_issue",
            "create project": "create_project",
            "new project": "create_project",
            "create pr": "create_pr",
            "pull request": "create_pr",
            "commit": "commit_changes",
            "push": "push_changes",
        }
        
        for keyword, action in github_actions.items():
            if keyword in command_lower:
                return {
                    "action": "github_operation",
                    "github_action": action,
                    "command": command
                }
        
        # Check for bug hunting operations
        bug_hunting_keywords = ["scan", "find bugs", "vulnerability", "security test", "bug hunt"]
        bug_hunting_actions = {
            "find bugs": "comprehensive_scan",
            "scan for bugs": "comprehensive_scan",
            "security scan": "comprehensive_scan",
            "vulnerability scan": "comprehensive_scan",
            "bug hunt": "comprehensive_scan",
            "quick scan": "quick_scan",
            "web scan": "web_scan",
            "sql injection": "sql_injection_test",
            "test sql": "sql_injection_test",
            "xss test": "xss_test",
            "check ssl": "ssl_check",
            "port scan": "port_scan",
            "directory scan": "directory_scan",
        }
        
        for keyword, action in bug_hunting_actions.items():
            if keyword in command_lower:
                return {
                    "action": "bug_hunting",
                    "bug_hunt_action": action,
                    "command": command
                }
        
        # Check for agent-specific commands
        if any(word in command_lower for word in ["scan", "recon", "port"]):
            return {"action": "recon", "agent": "recon"}
        
        if any(word in command_lower for word in ["code", "write", "generate"]):
            return {"action": "code_generation", "agent": "codegen"}
        
        if any(word in command_lower for word in ["explain", "teach", "learn"]):
            return {"action": "tutorial", "agent": "tutor"}
        
        if any(word in command_lower for word in ["security", "defend", "monitor"]):
            return {"action": "defense", "agent": "defender"}
        
        return {"action": "general", "agent": None}
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        health = self.auto_repair.get_health_status()
        
        return {
            "running": self.running,
            "execution_mode": self.execution_mode,
            "live_mode_enabled": self.live_mode_enabled,
            "teaching_mode_enabled": self.teaching_mode_enabled,
            "auto_repair_enabled": self.auto_repair_enabled,
            "health_status": health["status"],
            "agents": self.agent_manager.list_agents(),
            "plugins": self.plugin_manager.list_plugins(),
            "memory": {
                "short_term_entries": len(self.memory.short_term.history),
                "context_variables": len(self.memory.short_term.context)
            }
        }
    
    def get_conversation_history(self, last_n: int = 10) -> list:
        """Get recent conversation history"""
        return self.memory.short_term.get_history(last_n)
