"""
Recon Agent - Security reconnaissance and information gathering
"""
from typing import Dict, Any, List
from .base import BaseAgent, AgentRole, AgentStatus
from ..core.policy_engine import PolicyEngine, ActionResult
from ..core.logger import logger


class ReconAgent(BaseAgent):
    """
    Agent specialized in reconnaissance and information gathering.
    Performs security scans with strict authorization checks.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        super().__init__(
            name="recon",
            role=AgentRole.RECON,
            policy_engine=policy_engine
        )
        self.scan_history: List[Dict[str, Any]] = []
    
    def can_handle(self, task: str) -> bool:
        """Check if task is recon-related"""
        recon_keywords = [
            "scan", "recon", "enumerate", "discover",
            "port", "service", "network", "probe"
        ]
        return any(keyword in task.lower() for keyword in recon_keywords)
    
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute reconnaissance task"""
        self.set_status(AgentStatus.THINKING)
        
        target = context.get("target", "")
        scan_type = context.get("scan_type", "basic")
        
        # Check permission
        permission = self.check_permission("pentest.scan", target)
        
        if permission == ActionResult.DENIED:
            return {
                "success": False,
                "error": "Permission denied. Target not in allowed list.",
                "message": "Reconnaissance requires explicit authorization."
            }
        
        if permission == ActionResult.REQUIRES_CONFIRMATION:
            self.set_status(AgentStatus.WAITING_APPROVAL)
            return {
                "success": False,
                "requires_approval": True,
                "target": target,
                "scan_type": scan_type,
                "message": "Scan requires user confirmation"
            }
        
        logger.info(f"Performing {scan_type} scan on {target}")
        
        # Perform scan (placeholder - would use actual tools)
        results = self._perform_scan(target, scan_type)
        
        # Record scan
        self.scan_history.append({
            "target": target,
            "scan_type": scan_type,
            "results": results,
            "timestamp": logger
        })
        
        return {
            "success": True,
            "target": target,
            "scan_type": scan_type,
            "results": results,
            "message": "Scan completed successfully"
        }
    
    def _perform_scan(self, target: str, scan_type: str) -> Dict[str, Any]:
        """Perform scan (placeholder for actual tool integration)"""
        return {
            "target": target,
            "scan_type": scan_type,
            "status": "completed",
            "findings": [
                "This is a placeholder for actual scan results",
                "Would integrate with nmap, masscan, etc."
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """Return recon capabilities"""
        return [
            "port_scanning",
            "service_enumeration",
            "subdomain_discovery",
            "vulnerability_scanning",
            "network_mapping"
        ]
