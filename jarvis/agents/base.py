"""
Base classes for Jarvis agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

from ..core.logger import logger
from ..core.policy_engine import PolicyEngine, ActionResult


class AgentRole(Enum):
    """Agent role types"""
    SUPERVISOR = "supervisor"
    CODER = "coder"
    RECON = "recon"
    DEFENDER = "defender"
    TUTOR = "tutor"
    DATA_CURATOR = "data_curator"
    MONETIZATION_ADVISOR = "monetization_advisor"


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentMessage:
    """Message passed between agents"""
    
    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: str = "task",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.message_type = message_type
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()


class BaseAgent(ABC):
    """
    Base class for all Jarvis agents.
    Agents are autonomous components that can perform specific tasks.
    """
    
    def __init__(
        self,
        name: str,
        role: AgentRole,
        policy_engine: PolicyEngine
    ):
        self.name = name
        self.role = role
        self.policy_engine = policy_engine
        self.status = AgentStatus.IDLE
        self.context: Dict[str, Any] = {}
        self.memory: List[AgentMessage] = []
    
    @abstractmethod
    def can_handle(self, task: str) -> bool:
        """Check if agent can handle a specific task"""
        pass
    
    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task.
        
        Args:
            task: Task description
            context: Task context and parameters
        
        Returns:
            Dict with execution results
        """
        pass
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return []
    
    def check_permission(self, action: str, resource: str) -> ActionResult:
        """Check if action is allowed by policy"""
        return self.policy_engine.check_policy(
            action=action,
            resource=resource,
            user=self.name,
            metadata={"agent_role": self.role.value}
        )
    
    def requires_approval(self, action: str) -> bool:
        """Check if action requires user approval"""
        return self.policy_engine.requires_confirmation(action)
    
    def send_message(self, to_agent: str, content: str, message_type: str = "task") -> AgentMessage:
        """Send a message to another agent"""
        msg = AgentMessage(
            from_agent=self.name,
            to_agent=to_agent,
            content=content,
            message_type=message_type
        )
        self.memory.append(msg)
        logger.info(f"Agent {self.name} sent message to {to_agent}: {message_type}")
        return msg
    
    def receive_message(self, message: AgentMessage):
        """Receive a message from another agent"""
        self.memory.append(message)
        logger.info(f"Agent {self.name} received message from {message.from_agent}")
    
    def set_status(self, status: AgentStatus):
        """Update agent status"""
        self.status = status
        logger.debug(f"Agent {self.name} status: {status.value}")
    
    def log_action(self, action: str, result: str, metadata: Optional[Dict] = None):
        """Log agent action"""
        logger.info(f"Agent {self.name} - {action}: {result}")


class AgentOrchestrator:
    """Coordinates multiple agents"""
    
    def __init__(self, policy_engine: PolicyEngine):
        self.policy_engine = policy_engine
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[AgentMessage] = []
        logger.info("Agent orchestrator initialized")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent"""
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name} ({agent.role.value})")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self.agents.get(name)
    
    def find_capable_agent(self, task: str) -> Optional[BaseAgent]:
        """Find an agent capable of handling a task"""
        for agent in self.agents.values():
            if agent.can_handle(task) and agent.status == AgentStatus.IDLE:
                return agent
        return None
    
    async def route_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Route a task to appropriate agent"""
        agent = self.find_capable_agent(task)
        if not agent:
            logger.warning(f"No capable agent found for task: {task}")
            return {
                "success": False,
                "error": "No capable agent available"
            }
        
        logger.info(f"Routing task to agent: {agent.name}")
        agent.set_status(AgentStatus.EXECUTING)
        
        try:
            result = await agent.execute(task, context)
            agent.set_status(AgentStatus.COMPLETED)
            return result
        except Exception as e:
            logger.error(f"Agent {agent.name} failed: {e}")
            agent.set_status(AgentStatus.FAILED)
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_message(self, from_agent: str, to_agent: str, content: str):
        """Facilitate message passing between agents"""
        sender = self.agents.get(from_agent)
        receiver = self.agents.get(to_agent)
        
        if not sender or not receiver:
            logger.error(f"Invalid agent names: {from_agent} -> {to_agent}")
            return
        
        message = sender.send_message(to_agent, content)
        receiver.receive_message(message)
        self.message_queue.append(message)
