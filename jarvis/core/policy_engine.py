"""
Policy Engine - Security and permission management
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum

from .logger import logger, audit_logger


class ActionResult(Enum):
    """Result of policy check"""
    ALLOWED = "allowed"
    DENIED = "denied"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    DRY_RUN = "dry_run"


class PolicyEngine:
    """
    Manages security policies and permission checks.
    Every agent action must go through policy validation.
    """
    
    def __init__(self, policy_file: str = "data/policies/policies.json"):
        self.policy_file = Path(policy_file)
        self.policies: Dict[str, Any] = {}
        self.global_settings: Dict[str, Any] = {}
        self.trust_levels: Dict[str, Any] = {}
        self.rate_limits: Dict[str, List[datetime]] = {}
        
        self.load_policies()
    
    def load_policies(self):
        """Load policies from JSON file"""
        try:
            if self.policy_file.exists():
                with open(self.policy_file, 'r') as f:
                    data = json.load(f)
                    self.policies = data.get("policies", {})
                    self.global_settings = data.get("global_settings", {})
                    self.trust_levels = data.get("trust_levels", {})
                logger.info(f"Loaded {len(self.policies)} policies from {self.policy_file}")
            else:
                logger.warning(f"Policy file not found: {self.policy_file}")
                self._load_default_policies()
        except Exception as e:
            logger.error(f"Error loading policies: {e}")
            self._load_default_policies()
    
    def _load_default_policies(self):
        """Load minimal default policies"""
        self.policies = {
            "shell.execute": {
                "requires_confirmation": True,
                "sandbox_mode": True,
                "log_level": "verbose"
            },
            "file.write": {
                "requires_confirmation": True,
                "log_level": "verbose"
            }
        }
        self.global_settings = {
            "default_dry_run": False,
            "audit_all_actions": True
        }
    
    def check_policy(
        self,
        action: str,
        resource: str,
        user: str = "system",
        trust_level: str = "low",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ActionResult:
        """
        Check if an action is allowed by policy.
        
        Args:
            action: Action identifier (e.g., "pentest.scan", "file.write")
            resource: Resource being accessed
            user: User requesting the action
            trust_level: Current trust level (low, medium, high)
            metadata: Additional context for the policy check
        
        Returns:
            ActionResult indicating the policy decision
        """
        metadata = metadata or {}
        
        # Get policy for this action
        policy = self.policies.get(action, {})
        
        # Log the policy check
        audit_logger.log_action(
            action=f"policy_check.{action}",
            resource=resource,
            result="checking",
            user=user,
            metadata=metadata
        )
        
        # Check if action requires confirmation
        if policy.get("requires_confirmation", False):
            logger.info(f"Action {action} requires user confirmation")
            return ActionResult.REQUIRES_CONFIRMATION
        
        # Check if action requires supervisor approval
        if policy.get("requires_supervisor_approval", False):
            logger.info(f"Action {action} requires supervisor approval")
            return ActionResult.REQUIRES_CONFIRMATION
        
        # Check rate limits
        if not self._check_rate_limit(action, policy):
            logger.warning(f"Rate limit exceeded for action {action}")
            audit_logger.log_action(
                action=f"policy_check.{action}",
                resource=resource,
                result="denied_rate_limit",
                user=user,
                metadata=metadata
            )
            return ActionResult.DENIED
        
        # Check restricted paths for file operations
        if action.startswith("file."):
            if not self._check_file_policy(action, resource, policy):
                logger.warning(f"File operation {action} denied for {resource}")
                audit_logger.log_action(
                    action=f"policy_check.{action}",
                    resource=resource,
                    result="denied_restricted_path",
                    user=user,
                    metadata=metadata
                )
                return ActionResult.DENIED
        
        # Check command whitelist/blacklist for shell operations
        if action == "shell.execute":
            if not self._check_shell_policy(resource, policy):
                logger.warning(f"Shell command denied: {resource}")
                audit_logger.log_action(
                    action=f"policy_check.{action}",
                    resource=resource,
                    result="denied_blacklist",
                    user=user,
                    metadata=metadata
                )
                return ActionResult.DENIED
        
        # Check if dry run mode is enabled
        if policy.get("dry_run_default", False) or self.global_settings.get("default_dry_run", False):
            logger.info(f"Action {action} running in dry-run mode")
            return ActionResult.DRY_RUN
        
        # Action is allowed
        audit_logger.log_action(
            action=f"policy_check.{action}",
            resource=resource,
            result="allowed",
            user=user,
            metadata=metadata
        )
        return ActionResult.ALLOWED
    
    def _check_rate_limit(self, action: str, policy: Dict[str, Any]) -> bool:
        """Check if action is within rate limits"""
        if "rate_limit_per_hour" in policy:
            limit = policy["rate_limit_per_hour"]
            now = datetime.now()
            hour_ago = now - timedelta(hours=1)
            
            # Initialize or clean old entries
            if action not in self.rate_limits:
                self.rate_limits[action] = []
            self.rate_limits[action] = [
                ts for ts in self.rate_limits[action] if ts > hour_ago
            ]
            
            # Check limit
            if len(self.rate_limits[action]) >= limit:
                return False
            
            # Record this action
            self.rate_limits[action].append(now)
        
        return True
    
    def _check_file_policy(self, action: str, path: str, policy: Dict[str, Any]) -> bool:
        """Check file operation against policy"""
        restricted = policy.get("restricted_paths", [])
        
        # Expand home directory
        path_obj = Path(path).expanduser()
        
        # Check if path is in restricted list
        for restricted_path in restricted:
            restricted_obj = Path(restricted_path).expanduser()
            try:
                # Check if path is under restricted directory
                path_obj.resolve().relative_to(restricted_obj.resolve())
                return False
            except ValueError:
                # Path is not relative to restricted path
                continue
        
        return True
    
    def _check_shell_policy(self, command: str, policy: Dict[str, Any]) -> bool:
        """Check shell command against whitelist/blacklist"""
        # Check blacklist
        blacklist = policy.get("blacklist_commands", [])
        for blocked in blacklist:
            if blocked in command:
                return False
        
        # Check whitelist (if exists)
        whitelist = policy.get("whitelist_commands", [])
        if whitelist:
            # Extract first word (command name)
            cmd_name = command.strip().split()[0] if command.strip() else ""
            if cmd_name not in whitelist:
                return False
        
        return True
    
    def get_policy(self, action: str) -> Dict[str, Any]:
        """Get policy configuration for an action"""
        return self.policies.get(action, {})
    
    def requires_confirmation(self, action: str) -> bool:
        """Check if action requires user confirmation"""
        policy = self.get_policy(action)
        return policy.get("requires_confirmation", False)
