"""
Metasploit Plugin - Integration with Metasploit Framework
"""
from typing import Dict, Any, List, Optional
import subprocess
import json

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class MetasploitPlugin(JarvisPlugin):
    """
    Plugin for Metasploit Framework integration with teaching mode.
    """
    
    def __init__(self):
        super().__init__()
        self.teaching_mode = False
        self.session_active = False
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="metasploit",
            version="1.0.0",
            description="Metasploit Framework integration with teaching support",
            capabilities=[PluginCapability.SECURITY_TEST],
            permissions=["pentest.exploit", "pentest.scan"],
            author="Jarvis AI Team",
            dependencies=["metasploit-framework"]
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        
        # Check if msfconsole is available
        try:
            subprocess.run(
                ["msfconsole", "--version"],
                capture_output=True,
                check=True,
                timeout=10
            )
            logger.info("Metasploit plugin initialized")
            self.enabled = True
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("Metasploit not found - plugin disabled")
            self.enabled = False
            return False
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute Metasploit action"""
        if action == "search":
            return self._search_modules(**kwargs)
        elif action == "explain":
            return self._explain_module(**kwargs)
        elif action == "info":
            return self._module_info(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": ["search", "explain", "info"]
            }
    
    def _search_modules(
        self,
        query: str,
        module_type: Optional[str] = None,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Search for Metasploit modules"""
        if teaching is None:
            teaching = self.teaching_mode
        
        cmd = ["msfconsole", "-q", "-x", f"search {query}; exit"]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                "success": True,
                "query": query,
                "raw_output": result.stdout,
                "modules_found": self._parse_search_results(result.stdout)
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_metasploit": "Metasploit is a penetration testing framework with exploit modules",
                    "search_purpose": "Finding exploits and auxiliary modules for vulnerabilities",
                    "module_types": {
                        "exploit": "Code that takes advantage of a vulnerability",
                        "auxiliary": "Helper modules (scanners, fuzzers, etc.)",
                        "payload": "Code that runs after successful exploitation",
                        "post": "Post-exploitation modules"
                    },
                    "warning": "Only use on authorized systems with written permission"
                }
            
            return response
            
        except Exception as e:
            logger.error(f"Metasploit search error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _explain_module(self, module: str) -> Dict[str, Any]:
        """Explain what a module does"""
        return {
            "module": module,
            "explanation": "Metasploit module information",
            "recommendation": f"Use 'info {module}' in msfconsole for detailed information",
            "safety_reminder": "Always test in authorized environments only"
        }
    
    def _module_info(self, module: str, teaching: bool = None) -> Dict[str, Any]:
        """Get detailed module information"""
        if teaching is None:
            teaching = self.teaching_mode
        
        cmd = ["msfconsole", "-q", "-x", f"info {module}; exit"]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                "success": True,
                "module": module,
                "info": result.stdout
            }
            
            if teaching:
                response["learning_points"] = [
                    "Read the module description carefully",
                    "Check the disclosure date to understand vulnerability age",
                    "Review required options before running",
                    "Test in a lab environment first"
                ]
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_search_results(self, output: str) -> List[Dict[str, str]]:
        """Parse search results"""
        modules = []
        lines = output.split('\n')
        
        for line in lines:
            if 'exploit/' in line or 'auxiliary/' in line:
                parts = line.split()
                if parts:
                    modules.append({
                        "name": parts[0] if parts else "",
                        "line": line.strip()
                    })
        
        return modules
