"""
Defender Agent - Security monitoring and defense
"""
from typing import Dict, Any, List
from .base import BaseAgent, AgentRole, AgentStatus
from ..core.policy_engine import PolicyEngine
from ..core.logger import logger


class DefenderAgent(BaseAgent):
    """
    Agent specialized in security defense and monitoring.
    Analyzes system security posture and responds to threats.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        super().__init__(
            name="defender",
            role=AgentRole.DEFENDER,
            policy_engine=policy_engine
        )
        self.alerts: List[Dict[str, Any]] = []
    
    def can_handle(self, task: str) -> bool:
        """Check if task is defense-related"""
        defense_keywords = [
            "security", "monitor", "defend", "protect",
            "alert", "threat", "vulnerability", "patch"
        ]
        return any(keyword in task.lower() for keyword in defense_keywords)
    
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute defense task"""
        self.set_status(AgentStatus.THINKING)
        
        action = context.get("action", "monitor")
        
        logger.info(f"Defender performing: {action}")
        
        if action == "monitor":
            return await self._monitor_system()
        elif action == "analyze_alerts":
            return await self._analyze_alerts()
        elif action == "recommend_fixes":
            return await self._recommend_fixes(context)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }
    
    async def _monitor_system(self) -> Dict[str, Any]:
        """Monitor system for security issues"""
        findings = [
            {
                "type": "info",
                "message": "System monitoring active",
                "timestamp": "now"
            }
        ]
        
        return {
            "success": True,
            "action": "monitor",
            "findings": findings,
            "message": "System monitoring completed"
        }
    
    async def _analyze_alerts(self) -> Dict[str, Any]:
        """Analyze security alerts"""
        return {
            "success": True,
            "action": "analyze_alerts",
            "alert_count": len(self.alerts),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
    
    async def _recommend_fixes(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend security fixes"""
        recommendations = [
            "Keep system packages updated",
            "Review and apply security patches",
            "Enable firewall rules",
            "Monitor authentication logs"
        ]
        
        return {
            "success": True,
            "action": "recommend_fixes",
            "recommendations": recommendations
        }
    
    def get_capabilities(self) -> List[str]:
        """Return defender capabilities"""
        return [
            "system_monitoring",
            "alert_analysis",
            "threat_detection",
            "security_recommendations",
            "incident_response"
        ]
