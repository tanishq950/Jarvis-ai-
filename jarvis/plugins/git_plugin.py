"""
Git Plugin - Git operations with teaching mode
"""
from typing import Dict, Any, List, Optional
import subprocess
from pathlib import Path

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class GitPlugin(JarvisPlugin):
    """
    Plugin for Git operations with teaching support.
    """
    
    def __init__(self):
        super().__init__()
        self.teaching_mode = False
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="git",
            version="1.0.0",
            description="Git version control operations with teaching support",
            capabilities=[PluginCapability.FILE_OPERATION],
            permissions=["file.read", "file.write"],
            author="Jarvis AI Team"
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        self.enabled = True
        logger.info("Git plugin initialized")
        return True
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute git action"""
        actions = {
            "status": self._status,
            "diff": self._diff,
            "log": self._log,
            "clone": self._clone,
            "explain": self._explain_command
        }
        
        if action in actions:
            return actions[action](**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": list(actions.keys())
            }
    
    def _status(self, repo_path: str = ".", teaching: bool = None) -> Dict[str, Any]:
        """Get git status"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            response = {
                "success": True,
                "status": result.stdout,
                "repo_path": repo_path
            }
            
            if teaching:
                response["explanation"] = {
                    "command": "git status",
                    "purpose": "Show the working tree status",
                    "output_meaning": {
                        "M": "Modified file",
                        "A": "Added file (staged)",
                        "D": "Deleted file",
                        "??": "Untracked file",
                        "R": "Renamed file"
                    }
                }
            
            return response
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _diff(self, repo_path: str = ".", file: Optional[str] = None, teaching: bool = None) -> Dict[str, Any]:
        """Get git diff"""
        if teaching is None:
            teaching = self.teaching_mode
        
        cmd = ["git", "diff"]
        if file:
            cmd.append(file)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            response = {
                "success": True,
                "diff": result.stdout,
                "repo_path": repo_path,
                "file": file
            }
            
            if teaching:
                response["explanation"] = {
                    "command": "git diff",
                    "purpose": "Show changes between commits, working tree, and index",
                    "symbols": {
                        "+": "Line added",
                        "-": "Line removed",
                        "@@": "Chunk header showing line numbers"
                    }
                }
            
            return response
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _log(self, repo_path: str = ".", limit: int = 10, teaching: bool = None) -> Dict[str, Any]:
        """Get git log"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            result = subprocess.run(
                ["git", "log", f"-{limit}", "--oneline"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            response = {
                "success": True,
                "log": result.stdout,
                "commits": self._parse_log(result.stdout),
                "repo_path": repo_path
            }
            
            if teaching:
                response["explanation"] = {
                    "command": "git log",
                    "purpose": "Show commit history",
                    "format": "commit_hash commit_message"
                }
            
            return response
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _clone(self, url: str, destination: Optional[str] = None, teaching: bool = None) -> Dict[str, Any]:
        """Clone a git repository"""
        if teaching is None:
            teaching = self.teaching_mode
        
        cmd = ["git", "clone", url]
        if destination:
            cmd.append(destination)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            response = {
                "success": result.returncode == 0,
                "url": url,
                "destination": destination,
                "output": result.stdout
            }
            
            if teaching:
                response["explanation"] = {
                    "command": "git clone",
                    "purpose": "Create a local copy of a remote repository",
                    "what_happens": [
                        "Downloads all repository history",
                        "Creates a working directory",
                        "Sets up remote tracking"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _explain_command(self, command: str) -> Dict[str, Any]:
        """Explain a git command"""
        explanations = {
            "clone": "Create a copy of a remote repository",
            "status": "Show working tree status",
            "add": "Stage changes for commit",
            "commit": "Record changes to repository",
            "push": "Upload local changes to remote",
            "pull": "Download and merge remote changes",
            "branch": "List, create, or delete branches",
            "checkout": "Switch branches or restore files",
            "merge": "Join development histories",
            "diff": "Show changes between commits",
            "log": "Show commit history",
            "reset": "Undo changes",
            "rebase": "Reapply commits on another base"
        }
        
        return {
            "command": command,
            "explanation": explanations.get(command, "Git command"),
            "learn_more": f"Run 'git help {command}' for detailed information"
        }
    
    def _parse_log(self, log_output: str) -> List[Dict[str, str]]:
        """Parse git log output"""
        commits = []
        for line in log_output.strip().split('\n'):
            if line:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1]
                    })
        return commits
