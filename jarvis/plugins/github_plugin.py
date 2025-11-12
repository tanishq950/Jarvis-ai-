"""
GitHub Plugin - Integration with GitHub API
"""
from typing import Dict, Any, List, Optional
import subprocess
import json
import os

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class GitHubPlugin(JarvisPlugin):
    """
    Plugin for GitHub operations with teaching support.
    Create repos, manage projects, issues, PRs, and more.
    """
    
    def __init__(self):
        super().__init__()
        self.teaching_mode = False
        self.github_token = None
        self.username = None
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="github",
            version="1.0.0",
            description="GitHub integration for repository and project management",
            capabilities=[PluginCapability.FILE_OPERATION, PluginCapability.CODE_GENERATION],
            permissions=["file.write", "network.outbound"],
            author="Jarvis AI Team",
            dependencies=["PyGithub", "requests"]
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        
        # Get GitHub token from environment
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME")
        
        if not self.github_token:
            logger.warning("GITHUB_TOKEN not set - some features will be limited")
        
        self.enabled = True
        logger.info("GitHub plugin initialized")
        return True
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def enable_teaching_mode(self):
        """Enable teaching mode"""
        self.teaching_mode = True
    
    def disable_teaching_mode(self):
        """Disable teaching mode"""
        self.teaching_mode = False
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute GitHub action"""
        actions = {
            "create_repo": self._create_repo,
            "create_project": self._create_project,
            "create_issue": self._create_issue,
            "create_pr": self._create_pr,
            "list_repos": self._list_repos,
            "clone": self._clone_repo,
            "push": self._push_changes,
            "commit": self._commit_changes,
            "explain": self._explain_github,
        }
        
        if action in actions:
            return actions[action](**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": list(actions.keys())
            }
    
    def _create_repo(
        self,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = True,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create a new GitHub repository"""
        if teaching is None:
            teaching = self.teaching_mode
        
        if not self.github_token:
            return {
                "success": False,
                "error": "GitHub token not configured",
                "message": "Set GITHUB_TOKEN environment variable"
            }
        
        try:
            # Use GitHub CLI if available
            cmd = [
                "gh", "repo", "create", name,
                "--description", description,
                f"--{'private' if private else 'public'}"
            ]
            
            if auto_init:
                cmd.append("--add-readme")
            
            logger.info(f"Creating GitHub repository: {name}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                "success": result.returncode == 0,
                "repository": name,
                "description": description,
                "private": private,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_happened": f"Created a new {'private' if private else 'public'} repository on GitHub",
                    "repository_name": name,
                    "features": {
                        "auto_init": "Repository initialized with README" if auto_init else "Empty repository",
                        "visibility": "Private - only you can see it" if private else "Public - anyone can see it"
                    },
                    "next_steps": [
                        f"Clone the repository: git clone https://github.com/{self.username}/{name}.git",
                        "Add files to your repository",
                        "Commit and push changes",
                        "Invite collaborators if needed"
                    ],
                    "github_concepts": {
                        "repository": "A storage space for your project",
                        "README": "Main documentation file for your project",
                        "commits": "Snapshots of your code changes",
                        "branches": "Parallel versions of your code"
                    }
                }
            
            return response
            
        except FileNotFoundError:
            # Fallback to API call
            return self._create_repo_api(name, description, private, auto_init, teaching)
        except Exception as e:
            logger.error(f"Error creating repository: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_repo_api(
        self,
        name: str,
        description: str,
        private: bool,
        auto_init: bool,
        teaching: bool
    ) -> Dict[str, Any]:
        """Create repository using GitHub API"""
        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            data = {
                "name": name,
                "description": description,
                "private": private,
                "auto_init": auto_init
            }
            
            response = requests.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                repo_data = response.json()
                result = {
                    "success": True,
                    "repository": name,
                    "url": repo_data["html_url"],
                    "clone_url": repo_data["clone_url"],
                    "message": f"Repository created successfully at {repo_data['html_url']}"
                }
                
                if teaching:
                    result["explanation"] = self._get_repo_explanation(name, private)
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}",
                    "message": response.json().get("message", "Unknown error")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_project(
        self,
        repo: str,
        name: str,
        description: str = "",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create a GitHub project board"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = [
                "gh", "project", "create",
                "--title", name,
                "--body", description,
                "--repo", repo
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                "success": result.returncode == 0,
                "project": name,
                "repository": repo,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_project": "GitHub Projects are kanban-style boards for managing work",
                    "use_cases": [
                        "Track issues and pull requests",
                        "Organize tasks with cards",
                        "Plan sprints and milestones",
                        "Visualize workflow"
                    ],
                    "next_steps": [
                        "Add columns (To Do, In Progress, Done)",
                        "Create issues and add them to the project",
                        "Move cards as work progresses"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_issue(
        self,
        repo: str,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create a GitHub issue"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
            
            if labels:
                cmd.extend(["--label", ",".join(labels)])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                "success": result.returncode == 0,
                "issue": title,
                "repository": repo,
                "labels": labels or [],
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_issue": "Issues are used to track bugs, enhancements, and tasks",
                    "components": {
                        "title": "Brief description of the issue",
                        "body": "Detailed information and context",
                        "labels": "Categorize issues (bug, enhancement, etc.)",
                        "assignees": "People responsible for the issue",
                        "milestone": "Group issues by release or sprint"
                    },
                    "best_practices": [
                        "Use clear, descriptive titles",
                        "Include steps to reproduce for bugs",
                        "Add relevant labels",
                        "Reference related issues with #number"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_pr(
        self,
        repo: str,
        title: str,
        body: str = "",
        head: str = "main",
        base: str = "main",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create a pull request"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = [
                "gh", "pr", "create",
                "--repo", repo,
                "--title", title,
                "--body", body,
                "--head", head,
                "--base", base
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                "success": result.returncode == 0,
                "pull_request": title,
                "repository": repo,
                "head": head,
                "base": base,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_pr": "Pull Requests propose changes to a repository",
                    "workflow": [
                        "1. Create a branch with your changes",
                        "2. Push the branch to GitHub",
                        "3. Open a PR to merge into main branch",
                        "4. Review and discuss changes",
                        "5. Merge when approved"
                    ],
                    "best_practices": [
                        "Write clear PR descriptions",
                        "Keep PRs focused and small",
                        "Request reviews from team members",
                        "Respond to review comments",
                        "Update PR based on feedback"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _list_repos(self, teaching: bool = None) -> Dict[str, Any]:
        """List user's repositories"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["gh", "repo", "list", "--limit", "20"]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            repos = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        repos.append(line.split()[0])
            
            response = {
                "success": result.returncode == 0,
                "repositories": repos,
                "count": len(repos)
            }
            
            if teaching:
                response["explanation"] = {
                    "repositories_found": len(repos),
                    "what_you_can_do": [
                        "Clone a repository: gh repo clone <repo>",
                        "View repository: gh repo view <repo>",
                        "Create new repo: gh repo create <name>",
                        "Delete repo: gh repo delete <repo>"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _clone_repo(
        self,
        repo: str,
        directory: Optional[str] = None,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Clone a GitHub repository"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["gh", "repo", "clone", repo]
            if directory:
                cmd.append(directory)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            response = {
                "success": result.returncode == 0,
                "repository": repo,
                "directory": directory or repo.split('/')[-1],
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_happened": f"Created a local copy of {repo}",
                    "next_steps": [
                        f"cd {directory or repo.split('/')[-1]}",
                        "Explore the code",
                        "Make changes if needed",
                        "Create a branch for your changes",
                        "Commit and push your work"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _push_changes(
        self,
        repo_path: str = ".",
        branch: str = "main",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Push changes to GitHub"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["git", "push", "origin", branch]
            
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            response = {
                "success": result.returncode == 0,
                "branch": branch,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_happened": f"Uploaded your commits to GitHub on branch '{branch}'",
                    "git_workflow": [
                        "1. Make changes to files",
                        "2. Stage changes: git add <files>",
                        "3. Commit changes: git commit -m 'message'",
                        "4. Push to GitHub: git push"
                    ],
                    "troubleshooting": {
                        "rejected": "Pull latest changes first: git pull",
                        "conflict": "Resolve conflicts, then commit and push",
                        "authentication": "Check GitHub credentials"
                    }
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _commit_changes(
        self,
        message: str,
        files: Optional[List[str]] = None,
        repo_path: str = ".",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Commit changes"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            # Stage files
            if files:
                for file in files:
                    subprocess.run(
                        ["git", "add", file],
                        cwd=repo_path,
                        check=True
                    )
            else:
                subprocess.run(
                    ["git", "add", "."],
                    cwd=repo_path,
                    check=True
                )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            response = {
                "success": result.returncode == 0,
                "message": message,
                "files": files or ["all changes"],
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_commit": "A commit is a snapshot of your code at a point in time",
                    "commit_message_tips": [
                        "Be clear and concise",
                        "Use present tense (Add feature, not Added feature)",
                        "Explain what and why, not how",
                        "Reference issue numbers if applicable"
                    ],
                    "example_messages": [
                        "Add user authentication feature",
                        "Fix bug in payment processing",
                        "Update documentation for API endpoints",
                        "Refactor database connection logic"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _explain_github(self, topic: str = "basics") -> Dict[str, Any]:
        """Explain GitHub concepts"""
        explanations = {
            "basics": {
                "repository": "A project folder that tracks changes to your code",
                "commit": "A saved snapshot of your code",
                "branch": "A parallel version of your repository",
                "pull_request": "A proposal to merge changes from one branch to another",
                "issue": "A way to track bugs, features, and tasks",
                "fork": "Your own copy of someone else's repository"
            },
            "workflow": {
                "steps": [
                    "1. Create or clone a repository",
                    "2. Create a branch for your work",
                    "3. Make changes and commit them",
                    "4. Push your branch to GitHub",
                    "5. Open a pull request",
                    "6. Review and merge"
                ]
            },
            "collaboration": {
                "features": [
                    "Issues: Track bugs and features",
                    "Pull Requests: Review code changes",
                    "Projects: Organize work",
                    "Wiki: Documentation",
                    "Discussions: Community conversations"
                ]
            }
        }
        
        return {
            "success": True,
            "topic": topic,
            "explanation": explanations.get(topic, explanations["basics"])
        }
    
    def _get_repo_explanation(self, name: str, private: bool) -> Dict[str, Any]:
        """Get explanation for repository creation"""
        return {
            "repository_created": name,
            "visibility": "Private" if private else "Public",
            "what_next": [
                "Clone the repository to your local machine",
                "Add your code and files",
                "Commit your changes",
                "Push to GitHub",
                "Share with collaborators (if applicable)"
            ],
            "github_features": {
                "Issues": "Track bugs and feature requests",
                "Projects": "Organize tasks with kanban boards",
                "Actions": "Automate workflows (CI/CD)",
                "Wiki": "Create documentation",
                "Settings": "Configure repository options"
            }
        }
