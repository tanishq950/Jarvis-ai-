"""
Code Generation Agent
"""
from typing import Dict, Any, List
from .base import BaseAgent, AgentRole, AgentStatus
from ..core.policy_engine import PolicyEngine
from ..core.logger import logger


class CodeGenAgent(BaseAgent):
    """
    Agent specialized in code generation and modification.
    Generates code with review and static analysis.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        super().__init__(
            name="codegen",
            role=AgentRole.CODER,
            policy_engine=policy_engine
        )
    
    def can_handle(self, task: str) -> bool:
        """Check if task is code-related"""
        code_keywords = [
            "code", "program", "script", "function", "class",
            "implement", "write", "generate", "create file"
        ]
        return any(keyword in task.lower() for keyword in code_keywords)
    
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code generation task"""
        self.set_status(AgentStatus.THINKING)
        
        language = context.get("language", "python")
        file_path = context.get("file_path", "")
        
        # Check permission to write code
        permission = self.check_permission("code.generate", file_path)
        
        if self.requires_approval("code.generate"):
            self.set_status(AgentStatus.WAITING_APPROVAL)
            return {
                "success": False,
                "requires_approval": True,
                "message": "Code generation requires approval"
            }
        
        logger.info(f"Generating {language} code for: {task}")
        
        # Generate code template (placeholder - would integrate with LLM)
        code = self._generate_code_template(task, language)
        
        return {
            "success": True,
            "code": code,
            "language": language,
            "file_path": file_path,
            "requires_review": True,
            "message": "Code generated successfully. Review before execution."
        }
    
    def _generate_code_template(self, task: str, language: str) -> str:
        """Generate a code template (placeholder for LLM integration)"""
        if language == "python":
            return f'''"""
{task}
"""

def main():
    """Main function"""
    # TODO: Implement {task}
    pass


if __name__ == "__main__":
    main()
'''
        elif language == "bash":
            return f'''#!/bin/bash
# {task}

main() {{
    # TODO: Implement {task}
    echo "Not implemented yet"
}}

main "$@"
'''
        else:
            return f"# {task}\n# TODO: Implement in {language}"
    
    def get_capabilities(self) -> List[str]:
        """Return coder capabilities"""
        return [
            "generate_python_code",
            "generate_bash_scripts",
            "code_review",
            "refactoring",
            "static_analysis"
        ]
