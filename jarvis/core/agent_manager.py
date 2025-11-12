"""
Agent Manager - Manages agent lifecycle and coordination
"""
from typing import Dict, List, Optional, Any
from ..agents.base import BaseAgent, AgentRole, AgentStatus, AgentOrchestrator
from .policy_engine import PolicyEngine
from .logger import logger

# Import specific agents
from ..agents.supervisor import SupervisorAgent
from ..agents.codegen import CodeGenAgent
from ..agents.tutor import TutorAgent
from ..agents.recon import ReconAgent
from ..agents.defender import DefenderAgent


class AgentManager:
    """
    Central manager for all agents.
    Handles agent registration, lifecycle, and task routing.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        self.policy_engine = policy_engine
        self.orchestrator = AgentOrchestrator(policy_engine)
        self._initialize_agents()
        logger.info("Agent manager initialized")
    
    def _initialize_agents(self):
        """Initialize and register all agents"""
        # Create agents
        agents = [
            SupervisorAgent(self.policy_engine),
            CodeGenAgent(self.policy_engine),
            TutorAgent(self.policy_engine),
            ReconAgent(self.policy_engine),
            DefenderAgent(self.policy_engine)
        ]
        
        # Register each agent
        for agent in agents:
            self.orchestrator.register_agent(agent)
            logger.info(f"Registered agent: {agent.name} with role {agent.role.value}")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self.orchestrator.get_agent(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.orchestrator.agents.keys())
    
    def get_agent_status(self, name: str) -> Optional[str]:
        """Get the status of an agent"""
        agent = self.get_agent(name)
        if agent:
            return agent.status.value
        return None
    
    async def execute_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a task, either by a specific agent or by routing to capable agent.
        
        Args:
            task: Task description
            context: Task context
            agent_name: Specific agent to use (optional)
        
        Returns:
            Task execution results
        """
        context = context or {}
        
        if agent_name:
            # Execute with specific agent
            agent = self.get_agent(agent_name)
            if not agent:
                return {
                    "success": False,
                    "error": f"Agent not found: {agent_name}"
                }
            
            if not agent.can_handle(task):
                return {
                    "success": False,
                    "error": f"Agent {agent_name} cannot handle this task"
                }
            
            logger.info(f"Executing task with {agent_name}: {task}")
            return await agent.execute(task, context)
        else:
            # Route to capable agent
            logger.info(f"Routing task: {task}")
            return await self.orchestrator.route_task(task, context)
    
    def get_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all agents"""
        capabilities = {}
        for name, agent in self.orchestrator.agents.items():
            capabilities[name] = agent.get_capabilities()
        return capabilities
