"""
Auto-Repair System - Self-healing and error recovery
"""
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from datetime import datetime
import subprocess
import traceback

from ..core.logger import logger, audit_logger
from ..core.policy_engine import PolicyEngine


class IssueType(Enum):
    """Types of issues that can be detected"""
    DEPENDENCY_MISSING = "dependency_missing"
    CONFIGURATION_ERROR = "configuration_error"
    PERMISSION_DENIED = "permission_denied"
    SERVICE_DOWN = "service_down"
    FILE_MISSING = "file_missing"
    SYNTAX_ERROR = "syntax_error"
    NETWORK_ERROR = "network_error"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    TOOL_NOT_FOUND = "tool_not_found"


class RepairAction(Enum):
    """Types of repair actions"""
    INSTALL_PACKAGE = "install_package"
    FIX_PERMISSIONS = "fix_permissions"
    CREATE_FILE = "create_file"
    RESTART_SERVICE = "restart_service"
    FIX_CONFIGURATION = "fix_configuration"
    UPDATE_DEPENDENCIES = "update_dependencies"
    CLEAR_CACHE = "clear_cache"
    RESET_STATE = "reset_state"


class Issue:
    """Represents a detected issue"""
    
    def __init__(
        self,
        issue_type: IssueType,
        description: str,
        severity: str = "medium",
        component: str = "unknown",
        error_message: Optional[str] = None,
        suggested_fixes: Optional[List[str]] = None
    ):
        self.issue_type = issue_type
        self.description = description
        self.severity = severity
        self.component = component
        self.error_message = error_message
        self.suggested_fixes = suggested_fixes or []
        self.timestamp = datetime.utcnow().isoformat()
        self.resolved = False


class AutoRepairSystem:
    """
    Automatic repair and self-healing system.
    Detects issues and attempts to fix them automatically.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        self.policy_engine = policy_engine
        self.auto_repair_enabled = False
        self.detected_issues: List[Issue] = []
        self.repair_history: List[Dict[str, Any]] = []
        
        # Register repair strategies
        self.repair_strategies: Dict[IssueType, Callable] = {
            IssueType.DEPENDENCY_MISSING: self._repair_missing_dependency,
            IssueType.TOOL_NOT_FOUND: self._repair_missing_tool,
            IssueType.CONFIGURATION_ERROR: self._repair_configuration,
            IssueType.FILE_MISSING: self._repair_missing_file,
            IssueType.PERMISSION_DENIED: self._repair_permissions,
            IssueType.SERVICE_DOWN: self._repair_service,
        }
        
        logger.info("Auto-repair system initialized")
    
    def enable_auto_repair(self, confirm: bool = False) -> Dict[str, Any]:
        """Enable automatic repair"""
        if not confirm:
            return {
                "success": False,
                "message": "Auto-repair requires explicit confirmation",
                "warning": "Auto-repair will modify your system automatically!"
            }
        
        self.auto_repair_enabled = True
        logger.warning("⚠️  AUTO-REPAIR ENABLED - System will fix issues automatically")
        
        audit_logger.log_action(
            action="system.enable_auto_repair",
            resource="auto_repair",
            result="enabled"
        )
        
        return {
            "success": True,
            "message": "Auto-repair enabled. System will attempt to fix issues automatically.",
            "warning": "Use with caution - this modifies your system!"
        }
    
    def disable_auto_repair(self) -> Dict[str, Any]:
        """Disable automatic repair"""
        self.auto_repair_enabled = False
        logger.info("Auto-repair disabled")
        
        audit_logger.log_action(
            action="system.disable_auto_repair",
            resource="auto_repair",
            result="disabled"
        )
        
        return {
            "success": True,
            "message": "Auto-repair disabled."
        }
    
    def diagnose(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Issue:
        """
        Diagnose an error and identify the issue.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
        
        Returns:
            Issue object describing the problem
        """
        context = context or {}
        error_str = str(error)
        error_type = type(error).__name__
        
        logger.info(f"Diagnosing error: {error_type}: {error_str}")
        
        # Analyze error and determine issue type
        issue = self._analyze_error(error, error_str, error_type, context)
        
        # Store detected issue
        self.detected_issues.append(issue)
        
        logger.info(f"Diagnosed issue: {issue.issue_type.value} - {issue.description}")
        
        return issue
    
    def _analyze_error(
        self,
        error: Exception,
        error_str: str,
        error_type: str,
        context: Dict[str, Any]
    ) -> Issue:
        """Analyze error and create Issue object"""
        
        # Check for missing dependencies
        if "ModuleNotFoundError" in error_type or "ImportError" in error_type:
            module = self._extract_module_name(error_str)
            return Issue(
                issue_type=IssueType.DEPENDENCY_MISSING,
                description=f"Missing Python dependency: {module}",
                severity="high",
                component="dependencies",
                error_message=error_str,
                suggested_fixes=[f"pip install {module}"]
            )
        
        # Check for missing tools
        if "FileNotFoundError" in error_type or "command not found" in error_str.lower():
            tool = self._extract_tool_name(error_str, context)
            return Issue(
                issue_type=IssueType.TOOL_NOT_FOUND,
                description=f"Tool not found: {tool}",
                severity="high",
                component="tools",
                error_message=error_str,
                suggested_fixes=[f"apt install {tool}", f"which {tool}"]
            )
        
        # Check for permission errors
        if "PermissionError" in error_type or "Permission denied" in error_str:
            return Issue(
                issue_type=IssueType.PERMISSION_DENIED,
                description="Permission denied",
                severity="medium",
                component="permissions",
                error_message=error_str,
                suggested_fixes=["Run with appropriate permissions", "Check file ownership"]
            )
        
        # Check for configuration errors
        if "ConfigurationError" in error_type or "config" in error_str.lower():
            return Issue(
                issue_type=IssueType.CONFIGURATION_ERROR,
                description="Configuration error",
                severity="medium",
                component="configuration",
                error_message=error_str,
                suggested_fixes=["Check configuration files", "Reset to defaults"]
            )
        
        # Check for network errors
        if "ConnectionError" in error_type or "TimeoutError" in error_type:
            return Issue(
                issue_type=IssueType.NETWORK_ERROR,
                description="Network connectivity issue",
                severity="medium",
                component="network",
                error_message=error_str,
                suggested_fixes=["Check network connection", "Verify firewall settings"]
            )
        
        # Generic issue
        return Issue(
            issue_type=IssueType.CONFIGURATION_ERROR,
            description=f"Unknown error: {error_type}",
            severity="low",
            component="unknown",
            error_message=error_str,
            suggested_fixes=["Check logs for details", "Contact support"]
        )
    
    def repair(self, issue: Issue, auto: bool = None) -> Dict[str, Any]:
        """
        Attempt to repair an issue.
        
        Args:
            issue: The issue to repair
            auto: Whether to repair automatically (overrides global setting)
        
        Returns:
            Repair results
        """
        if auto is None:
            auto = self.auto_repair_enabled
        
        if not auto:
            return {
                "success": False,
                "requires_approval": True,
                "issue": issue.description,
                "suggested_fixes": issue.suggested_fixes,
                "message": "Auto-repair disabled. Manual intervention required."
            }
        
        logger.info(f"Attempting to repair: {issue.description}")
        
        # Get repair strategy
        strategy = self.repair_strategies.get(issue.issue_type)
        
        if not strategy:
            logger.warning(f"No repair strategy for {issue.issue_type.value}")
            return {
                "success": False,
                "issue": issue.description,
                "message": f"No automatic repair available for {issue.issue_type.value}",
                "suggested_fixes": issue.suggested_fixes
            }
        
        # Check policy permission
        permission = self.policy_engine.check_policy(
            action="system.repair",
            resource=issue.issue_type.value
        )
        
        # Attempt repair
        try:
            result = strategy(issue)
            
            # Record repair attempt
            self.repair_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "issue": issue.description,
                "issue_type": issue.issue_type.value,
                "success": result.get("success", False),
                "actions_taken": result.get("actions_taken", [])
            })
            
            if result.get("success"):
                issue.resolved = True
                logger.info(f"Successfully repaired: {issue.description}")
                
                audit_logger.log_action(
                    action="system.repair",
                    resource=issue.issue_type.value,
                    result="success",
                    metadata={"issue": issue.description}
                )
            else:
                logger.warning(f"Repair failed: {issue.description}")
            
            return result
            
        except Exception as e:
            logger.error(f"Repair error: {e}")
            return {
                "success": False,
                "issue": issue.description,
                "error": str(e),
                "message": "Repair attempt failed"
            }
    
    def _repair_missing_dependency(self, issue: Issue) -> Dict[str, Any]:
        """Repair missing Python dependency"""
        module = self._extract_module_name(issue.error_message or "")
        
        logger.info(f"Installing missing dependency: {module}")
        
        try:
            result = subprocess.run(
                ["pip", "install", module],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Successfully installed {module}",
                    "actions_taken": [f"pip install {module}"],
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to install {module}",
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error installing {module}",
                "error": str(e)
            }
    
    def _repair_missing_tool(self, issue: Issue) -> Dict[str, Any]:
        """Repair missing system tool"""
        tool = self._extract_tool_name(issue.error_message or "", {})
        
        logger.info(f"Installing missing tool: {tool}")
        
        # Check if we're on Kali/Debian
        try:
            result = subprocess.run(
                ["which", "apt-get"],
                capture_output=True
            )
            
            if result.returncode == 0:
                # Use apt-get to install
                install_result = subprocess.run(
                    ["sudo", "apt-get", "install", "-y", tool],
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if install_result.returncode == 0:
                    return {
                        "success": True,
                        "message": f"Successfully installed {tool}",
                        "actions_taken": [f"apt-get install {tool}"]
                    }
            
            return {
                "success": False,
                "message": f"Could not install {tool}",
                "suggested_fixes": [
                    f"Manually install: sudo apt-get install {tool}",
                    f"Or use appropriate package manager"
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error installing {tool}",
                "error": str(e)
            }
    
    def _repair_configuration(self, issue: Issue) -> Dict[str, Any]:
        """Repair configuration issues"""
        logger.info("Attempting configuration repair")
        
        actions = []
        
        # Try to recreate missing configuration files
        from pathlib import Path
        
        config_files = [
            ".env",
            "jarvis/data/policies/policies.json"
        ]
        
        for config_file in config_files:
            path = Path(config_file)
            if not path.exists() and path.with_suffix(".example").exists():
                # Copy from example
                import shutil
                shutil.copy(
                    str(path.with_suffix(".example")),
                    str(path)
                )
                actions.append(f"Created {config_file} from example")
        
        if actions:
            return {
                "success": True,
                "message": "Configuration repaired",
                "actions_taken": actions
            }
        
        return {
            "success": False,
            "message": "Could not automatically repair configuration",
            "suggested_fixes": issue.suggested_fixes
        }
    
    def _repair_missing_file(self, issue: Issue) -> Dict[str, Any]:
        """Repair missing file issues"""
        return {
            "success": False,
            "message": "Cannot automatically create missing files",
            "suggested_fixes": issue.suggested_fixes
        }
    
    def _repair_permissions(self, issue: Issue) -> Dict[str, Any]:
        """Repair permission issues"""
        return {
            "success": False,
            "message": "Permission issues require manual intervention",
            "suggested_fixes": [
                "Check file/directory permissions",
                "Run with appropriate user privileges",
                "Use sudo if necessary"
            ]
        }
    
    def _repair_service(self, issue: Issue) -> Dict[str, Any]:
        """Repair service issues"""
        return {
            "success": False,
            "message": "Service management requires manual intervention",
            "suggested_fixes": issue.suggested_fixes
        }
    
    def _extract_module_name(self, error_str: str) -> str:
        """Extract module name from error message"""
        # Try to extract from "No module named 'xxx'"
        if "No module named" in error_str:
            import re
            match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_str)
            if match:
                return match.group(1).split('.')[0]  # Get top-level package
        
        # Try to extract from "ModuleNotFoundError: xxx"
        if ":" in error_str:
            parts = error_str.split(":")
            if len(parts) > 1:
                return parts[-1].strip().strip("'\"")
        
        return "unknown"
    
    def _extract_tool_name(self, error_str: str, context: Dict[str, Any]) -> str:
        """Extract tool name from error message or context"""
        # Check context first
        if "command" in context:
            cmd = context["command"]
            if isinstance(cmd, str):
                return cmd.split()[0]
            elif isinstance(cmd, list):
                return cmd[0]
        
        # Try to extract from error
        if "command not found" in error_str.lower():
            import re
            match = re.search(r"(\w+):.*command not found", error_str)
            if match:
                return match.group(1)
        
        return "unknown"
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """Get system diagnostics"""
        return {
            "auto_repair_enabled": self.auto_repair_enabled,
            "total_issues_detected": len(self.detected_issues),
            "unresolved_issues": len([i for i in self.detected_issues if not i.resolved]),
            "repair_attempts": len(self.repair_history),
            "recent_issues": [
                {
                    "type": i.issue_type.value,
                    "description": i.description,
                    "severity": i.severity,
                    "resolved": i.resolved,
                    "timestamp": i.timestamp
                }
                for i in self.detected_issues[-10:]
            ],
            "recent_repairs": self.repair_history[-10:]
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health"""
        unresolved = [i for i in self.detected_issues if not i.resolved]
        critical = [i for i in unresolved if i.severity == "high"]
        
        if critical:
            health = "critical"
        elif len(unresolved) > 5:
            health = "degraded"
        elif unresolved:
            health = "warning"
        else:
            health = "healthy"
        
        return {
            "status": health,
            "unresolved_issues": len(unresolved),
            "critical_issues": len(critical),
            "auto_repair_enabled": self.auto_repair_enabled,
            "message": self._get_health_message(health, len(unresolved), len(critical))
        }
    
    def _get_health_message(self, health: str, unresolved: int, critical: int) -> str:
        """Get health status message"""
        if health == "healthy":
            return "System is healthy"
        elif health == "warning":
            return f"{unresolved} minor issues detected"
        elif health == "degraded":
            return f"{unresolved} issues affecting system"
        else:
            return f"{critical} critical issues require attention"
