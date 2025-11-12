"""
Supervisor Agent - Oversees and approves agent actions
"""
from typing import Dict, Any, List
from .base import BaseAgent, AgentRole, AgentStatus
from ..core.policy_engine import PolicyEngine, ActionResult
from ..core.logger import logger


class SupervisorAgent(BaseAgent):
    """
    Supervisor agent that reviews and approves actions from other agents.
    Acts as a safety layer for high-risk operations.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        super().__init__(
            name="supervisor",
            role=AgentRole.SUPERVISOR,
            policy_engine=policy_engine
        )
        self.pending_approvals: List[Dict[str, Any]] = []
    
    def can_handle(self, task: str) -> bool:
        """Supervisor can handle approval requests"""
        approval_keywords = ["approve", "review", "permission", "authorize"]
        return any(keyword in task.lower() for keyword in approval_keywords)
    
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute supervisor task"""
        self.set_status(AgentStatus.THINKING)
        
        action_type = context.get("action_type", "unknown")
        requesting_agent = context.get("agent", "unknown")
        resource = context.get("resource", "")
        
        logger.info(f"Supervisor reviewing: {action_type} by {requesting_agent}")
        
        # Check policy
        policy_result = self.check_permission(action_type, resource)
        
        if policy_result == ActionResult.DENIED:
            return {
                "success": False,
                "approved": False,
                "reason": "Policy violation",
                "action": action_type
            }
        
        # Assess risk level
        risk_level = self._assess_risk(action_type, resource, context)
        
        if risk_level == "high":
            # High risk requires explicit user confirmation
            return {
                "success": True,
                "approved": False,
                "requires_user_confirmation": True,
                "risk_level": risk_level,
                "reason": "High-risk operation requires user approval",
                "action": action_type
            }
        elif risk_level == "medium":
            # Medium risk: auto-approve with logging
            logger.warning(f"Auto-approving medium risk action: {action_type}")
            return {
                "success": True,
                "approved": True,
                "risk_level": risk_level,
                "action": action_type
            }
        else:
            # Low risk: approve
            return {
                "success": True,
                "approved": True,
                "risk_level": risk_level,
                "action": action_type
            }
    
    def _assess_risk(self, action: str, resource: str, context: Dict[str, Any]) -> str:
        """
        Assess risk level of an action.
        Returns: "low", "medium", or "high"
        """
        # High risk actions
        high_risk_actions = [
            "pentest.exploit",
            "file.delete",
            "system.install",
            "shell.execute"
        ]
        
        # Medium risk actions
        medium_risk_actions = [
            "pentest.scan",
            "file.write",
            "network.scan",
            "code.execute"
        ]
        
        if any(action.startswith(risk) for risk in high_risk_actions):
            return "high"
        elif any(action.startswith(risk) for risk in medium_risk_actions):
            return "medium"
        else:
            return "low"
    
    def get_capabilities(self) -> List[str]:
        """Return supervisor capabilities"""
        return [
            "approve_actions",
            "assess_risk",
            "policy_enforcement",
            "audit_review"
        ]
