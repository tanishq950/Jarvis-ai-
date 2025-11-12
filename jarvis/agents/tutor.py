"""
Tutor Agent - Explains concepts and provides learning support
"""
from typing import Dict, Any, List
from .base import BaseAgent, AgentRole, AgentStatus
from ..core.policy_engine import PolicyEngine
from ..core.logger import logger


class TutorAgent(BaseAgent):
    """
    Agent specialized in teaching and explaining concepts.
    Provides step-by-step guidance and learning materials.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        super().__init__(
            name="tutor",
            role=AgentRole.TUTOR,
            policy_engine=policy_engine
        )
        self.learning_profile: Dict[str, Any] = {
            "topics_covered": [],
            "weak_areas": [],
            "preferred_style": "detailed"
        }
    
    def can_handle(self, task: str) -> bool:
        """Check if task is learning-related"""
        learning_keywords = [
            "explain", "teach", "how does", "what is",
            "tutorial", "learn", "understand", "guide"
        ]
        return any(keyword in task.lower() for keyword in learning_keywords)
    
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tutoring task"""
        self.set_status(AgentStatus.THINKING)
        
        topic = context.get("topic", task)
        detail_level = context.get("detail_level", "medium")
        
        logger.info(f"Explaining topic: {topic}")
        
        # Generate explanation
        explanation = self._generate_explanation(topic, detail_level)
        
        # Track learning
        self.learning_profile["topics_covered"].append(topic)
        
        return {
            "success": True,
            "topic": topic,
            "explanation": explanation,
            "examples": self._get_examples(topic),
            "next_steps": self._suggest_next_steps(topic),
            "message": "Explanation provided"
        }
    
    def _generate_explanation(self, topic: str, detail_level: str) -> str:
        """Generate explanation (placeholder for LLM integration)"""
        explanations = {
            "pentest": """
Penetration testing (pentesting) is a simulated cyber attack against your system 
to check for exploitable vulnerabilities. Key concepts:

1. Reconnaissance: Gathering information about the target
2. Scanning: Identifying open ports and services
3. Enumeration: Extracting detailed information
4. Exploitation: Attempting to gain access
5. Post-exploitation: Maintaining access and extracting data
6. Reporting: Documenting findings

Important: Always get written authorization before testing any system.
""",
            "code": """
Code generation involves creating functional programs from specifications.
Best practices:
1. Understand requirements clearly
2. Plan your approach
3. Write clean, readable code
4. Include error handling
5. Add documentation
6. Test thoroughly
""",
        }
        
        # Try to match topic
        for key, value in explanations.items():
            if key in topic.lower():
                return value
        
        return f"Explanation for: {topic}\n(Placeholder - would use LLM for detailed explanation)"
    
    def _get_examples(self, topic: str) -> List[str]:
        """Get examples for the topic"""
        examples = {
            "pentest": [
                "nmap -sV -p- target.com",
                "Use Burp Suite to test web applications",
                "Check for SQL injection vulnerabilities"
            ],
            "code": [
                "Write unit tests for your functions",
                "Use meaningful variable names",
                "Follow PEP 8 style guide for Python"
            ]
        }
        
        for key, value in examples.items():
            if key in topic.lower():
                return value
        
        return ["Example would be generated here"]
    
    def _suggest_next_steps(self, topic: str) -> List[str]:
        """Suggest next learning steps"""
        return [
            f"Practice {topic} with hands-on exercises",
            "Review related documentation",
            "Try implementing a small project"
        ]
    
    def get_capabilities(self) -> List[str]:
        """Return tutor capabilities"""
        return [
            "explain_concepts",
            "provide_tutorials",
            "suggest_learning_path",
            "create_quizzes",
            "track_progress"
        ]
