"""
Shell Execution Plugin - Safe wrapper for shell commands
"""
from typing import Dict, Any, List, Optional
import subprocess
import shlex
from pathlib import Path

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger, audit_logger


class ShellPlugin(JarvisPlugin):
    """
    Plugin for executing shell commands with safety checks.
    Supports all Kali Linux tools with proper sandboxing.
    """
    
    def __init__(self):
        super().__init__()
        self.command_history: List[Dict[str, Any]] = []
        self.teaching_mode = False
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="shell",
            version="1.0.0",
            description="Execute shell commands and Kali Linux tools",
            capabilities=[PluginCapability.SYSTEM_COMMAND],
            permissions=["shell.execute"],
            author="Jarvis AI Team"
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        self.enabled = True
        logger.info("Shell plugin initialized")
        return True
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def enable_teaching_mode(self):
        """Enable teaching mode"""
        self.teaching_mode = True
        logger.info("Shell plugin teaching mode enabled")
    
    def disable_teaching_mode(self):
        """Disable teaching mode"""
        self.teaching_mode = False
        logger.info("Shell plugin teaching mode disabled")
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute shell command.
        
        Args:
            action: Action type ('run', 'explain', 'dry_run')
            command: Command to execute
            timeout: Execution timeout in seconds
            working_dir: Working directory
            capture_output: Whether to capture output
        """
        if action == "run":
            return self._run_command(**kwargs)
        elif action == "explain":
            return self._explain_command(**kwargs)
        elif action == "dry_run":
            return self._dry_run(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }
    
    def _run_command(
        self,
        command: str,
        timeout: int = 300,
        working_dir: Optional[str] = None,
        capture_output: bool = True,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Execute a shell command"""
        # Use plugin teaching mode if not specified
        if teaching is None:
            teaching = self.teaching_mode
        
        # Get explanation first if in teaching mode
        explanation = None
        if teaching:
            explanation = self._explain_command(command=command)
        
        try:
            # Parse command safely
            cmd_parts = shlex.split(command)
            
            # Log the command
            audit_logger.log_action(
                action="shell.execute",
                resource=command,
                result="executing",
                metadata={"working_dir": working_dir}
            )
            
            # Execute command
            logger.info(f"Executing: {command}")
            
            result = subprocess.run(
                cmd_parts,
                timeout=timeout,
                cwd=working_dir,
                capture_output=capture_output,
                text=True
            )
            
            # Store in history
            history_entry = {
                "command": command,
                "returncode": result.returncode,
                "success": result.returncode == 0,
                "working_dir": working_dir
            }
            self.command_history.append(history_entry)
            
            # Log result
            audit_logger.log_action(
                action="shell.execute",
                resource=command,
                result="success" if result.returncode == 0 else "failed",
                metadata={"returncode": result.returncode}
            )
            
            response = {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "command": command
            }
            
            if capture_output:
                response["stdout"] = result.stdout
                response["stderr"] = result.stderr
            
            if teaching and explanation:
                response["explanation"] = explanation
                response["teaching_mode"] = True
            
            return response
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return {
                "success": False,
                "error": "Command execution timeout",
                "command": command
            }
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    def _explain_command(self, command: str) -> Dict[str, Any]:
        """Explain what a command does"""
        cmd_parts = shlex.split(command) if command else []
        if not cmd_parts:
            return {"explanation": "Empty command"}
        
        tool = cmd_parts[0]
        
        # Kali Linux tools explanations
        explanations = self._get_tool_explanations()
        
        tool_info = explanations.get(tool, {
            "description": f"Command: {tool}",
            "usage": "See man page or --help for usage",
            "purpose": "General command"
        })
        
        # Build full explanation
        explanation = {
            "tool": tool,
            "full_command": command,
            "description": tool_info.get("description"),
            "purpose": tool_info.get("purpose"),
            "usage": tool_info.get("usage"),
            "arguments": self._parse_arguments(cmd_parts[1:]),
            "warnings": tool_info.get("warnings", []),
            "examples": tool_info.get("examples", [])
        }
        
        return explanation
    
    def _dry_run(self, command: str, **kwargs) -> Dict[str, Any]:
        """Show what would be executed without running"""
        explanation = self._explain_command(command)
        
        return {
            "success": True,
            "dry_run": True,
            "command": command,
            "would_execute": command,
            "explanation": explanation,
            "message": "This is a dry run - command not executed"
        }
    
    def _parse_arguments(self, args: List[str]) -> List[Dict[str, str]]:
        """Parse command arguments"""
        parsed = []
        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith('-'):
                # It's a flag
                value = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('-') else None
                parsed.append({
                    "flag": arg,
                    "value": value,
                    "description": self._explain_flag(arg)
                })
                if value:
                    i += 2
                else:
                    i += 1
            else:
                parsed.append({
                    "argument": arg,
                    "description": "Target or parameter"
                })
                i += 1
        return parsed
    
    def _explain_flag(self, flag: str) -> str:
        """Explain common flags"""
        flag_explanations = {
            "-h": "Show help",
            "--help": "Show help",
            "-v": "Verbose output",
            "-V": "Show version",
            "--version": "Show version",
            "-o": "Output file",
            "-p": "Port",
            "-n": "No prompt/numeric",
            "-a": "All/append",
            "-r": "Recursive",
            "-f": "Force",
            "-i": "Interactive",
            "-q": "Quiet",
        }
        return flag_explanations.get(flag, "See documentation")
    
    def _get_tool_explanations(self) -> Dict[str, Dict[str, Any]]:
        """Get explanations for Kali Linux tools"""
        return {
            # Network Tools
            "nmap": {
                "description": "Network Mapper - Network discovery and security auditing",
                "purpose": "Scan networks to discover hosts, services, and vulnerabilities",
                "usage": "nmap [options] target",
                "warnings": ["Requires authorization to scan networks", "Can be detected by IDS/IPS"],
                "examples": [
                    "nmap -sV target.com  # Service version detection",
                    "nmap -p 80,443 target.com  # Scan specific ports",
                    "nmap -sn 192.168.1.0/24  # Ping scan"
                ]
            },
            "netcat": {
                "description": "Network Swiss Army knife - Read/write network connections",
                "purpose": "Create network connections, port scanning, file transfer",
                "usage": "nc [options] host port",
                "examples": ["nc -lvp 4444  # Listen on port 4444"]
            },
            "nc": {
                "description": "Netcat - Network utility",
                "purpose": "TCP/UDP connections and listeners",
                "usage": "nc [options] host port"
            },
            "wireshark": {
                "description": "Network protocol analyzer",
                "purpose": "Capture and analyze network packets",
                "usage": "wireshark [options]",
                "warnings": ["May capture sensitive data"]
            },
            
            # Web Tools
            "burpsuite": {
                "description": "Web application security testing platform",
                "purpose": "Test web application security",
                "usage": "burpsuite",
                "warnings": ["Only test applications you own or have permission to test"]
            },
            "nikto": {
                "description": "Web server scanner",
                "purpose": "Scan web servers for vulnerabilities",
                "usage": "nikto -h target",
                "warnings": ["Requires authorization"]
            },
            "sqlmap": {
                "description": "Automatic SQL injection tool",
                "purpose": "Detect and exploit SQL injection vulnerabilities",
                "usage": "sqlmap -u URL",
                "warnings": ["Only use on authorized targets", "Can modify databases"]
            },
            "dirb": {
                "description": "Web content scanner",
                "purpose": "Find hidden web directories and files",
                "usage": "dirb http://target"
            },
            "gobuster": {
                "description": "Directory/file brute-forcer",
                "purpose": "Discover hidden paths on web servers",
                "usage": "gobuster dir -u URL -w wordlist"
            },
            
            # Password Tools
            "hydra": {
                "description": "Network login cracker",
                "purpose": "Brute force network services",
                "usage": "hydra [options] target service",
                "warnings": ["Illegal without authorization", "Can lock accounts"]
            },
            "john": {
                "description": "John the Ripper - Password cracker",
                "purpose": "Crack password hashes",
                "usage": "john [options] password_file"
            },
            "hashcat": {
                "description": "Advanced password recovery",
                "purpose": "Crack password hashes using GPU",
                "usage": "hashcat -m mode -a attack hash"
            },
            
            # Exploitation
            "metasploit": {
                "description": "Penetration testing framework",
                "purpose": "Develop and execute exploit code",
                "usage": "msfconsole",
                "warnings": ["Use only on authorized systems", "Can cause system damage"]
            },
            "msfconsole": {
                "description": "Metasploit console",
                "purpose": "Interactive Metasploit interface",
                "usage": "msfconsole"
            },
            
            # Wireless
            "aircrack-ng": {
                "description": "WiFi security auditing tools",
                "purpose": "Test WiFi network security",
                "usage": "aircrack-ng [options] capture_file",
                "warnings": ["Illegal to crack networks without permission"]
            },
            "airodump-ng": {
                "description": "WiFi packet capture",
                "purpose": "Capture WiFi packets",
                "usage": "airodump-ng interface"
            },
            
            # Information Gathering
            "whois": {
                "description": "Domain registration information lookup",
                "purpose": "Get domain registration details",
                "usage": "whois domain.com"
            },
            "dig": {
                "description": "DNS lookup tool",
                "purpose": "Query DNS servers",
                "usage": "dig domain.com"
            },
            "theHarvester": {
                "description": "OSINT gathering tool",
                "purpose": "Gather emails, subdomains, IPs from public sources",
                "usage": "theHarvester -d domain.com -b google"
            },
            "maltego": {
                "description": "OSINT and forensics platform",
                "purpose": "Visualize relationships in data",
                "usage": "maltego"
            },
            
            # Exploitation Frameworks
            "beef": {
                "description": "Browser Exploitation Framework",
                "purpose": "Test browser vulnerabilities",
                "usage": "beef-xss",
                "warnings": ["Only use on authorized targets"]
            },
            
            # Forensics
            "autopsy": {
                "description": "Digital forensics platform",
                "purpose": "Analyze disk images and files",
                "usage": "autopsy"
            },
            "volatility": {
                "description": "Memory forensics framework",
                "purpose": "Analyze memory dumps",
                "usage": "volatility -f memory.dump plugin"
            },
            
            # Reverse Engineering
            "ghidra": {
                "description": "Software reverse engineering suite",
                "purpose": "Analyze compiled code",
                "usage": "ghidra"
            },
            "radare2": {
                "description": "Reverse engineering framework",
                "purpose": "Analyze and debug binaries",
                "usage": "r2 binary"
            },
            
            # Sniffing
            "tcpdump": {
                "description": "Network packet analyzer",
                "purpose": "Capture network traffic",
                "usage": "tcpdump -i interface",
                "warnings": ["May require root privileges"]
            },
            "ettercap": {
                "description": "Network sniffer/interceptor",
                "purpose": "Man-in-the-middle attacks",
                "usage": "ettercap -G",
                "warnings": ["Highly invasive - requires authorization"]
            }
        }
    
    def get_command_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent command history"""
        return self.command_history[-limit:]
