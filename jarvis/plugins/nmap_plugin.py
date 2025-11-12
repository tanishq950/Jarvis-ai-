"""
Nmap Plugin - Network scanning with Nmap
"""
from typing import Dict, Any, List, Optional
import subprocess
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class NmapPlugin(JarvisPlugin):
    """
    Plugin for Nmap network scanning with teaching mode.
    """
    
    def __init__(self):
        super().__init__()
        self.scan_history: List[Dict[str, Any]] = []
        self.teaching_mode = False
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="nmap",
            version="1.0.0",
            description="Nmap network scanner with teaching support",
            capabilities=[PluginCapability.NETWORK_SCAN, PluginCapability.SECURITY_TEST],
            permissions=["pentest.scan", "network.scan"],
            author="Jarvis AI Team"
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        self.enabled = True
        
        # Check if nmap is available
        try:
            subprocess.run(["nmap", "--version"], capture_output=True, check=True)
            logger.info("Nmap plugin initialized")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Nmap not found - plugin disabled")
            self.enabled = False
            return False
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute nmap action"""
        if action == "scan":
            return self._scan(**kwargs)
        elif action == "explain":
            return self._explain_scan(**kwargs)
        elif action == "quick_scan":
            return self._quick_scan(**kwargs)
        elif action == "service_scan":
            return self._service_scan(**kwargs)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    def _scan(
        self,
        target: str,
        flags: str = "-sV",
        timeout: int = 600,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Perform nmap scan"""
        if teaching is None:
            teaching = self.teaching_mode
        
        # Build command
        cmd = ["nmap"] + flags.split() + [target]
        
        # Get explanation if teaching
        explanation = None
        if teaching:
            explanation = self._explain_scan(target=target, flags=flags)
        
        try:
            logger.info(f"Running nmap scan: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                timeout=timeout,
                capture_output=True,
                text=True
            )
            
            # Parse results
            parsed = self._parse_output(result.stdout)
            
            # Store in history
            self.scan_history.append({
                "target": target,
                "flags": flags,
                "success": result.returncode == 0,
                "parsed": parsed
            })
            
            response = {
                "success": result.returncode == 0,
                "target": target,
                "raw_output": result.stdout,
                "parsed": parsed,
                "command": " ".join(cmd)
            }
            
            if teaching and explanation:
                response["explanation"] = explanation
                response["learning_points"] = self._get_learning_points(flags)
            
            return response
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Scan timeout",
                "target": target
            }
        except Exception as e:
            logger.error(f"Nmap scan error: {e}")
            return {
                "success": False,
                "error": str(e),
                "target": target
            }
    
    def _quick_scan(self, target: str, teaching: bool = None) -> Dict[str, Any]:
        """Quick scan of common ports"""
        return self._scan(
            target=target,
            flags="-T4 -F",
            teaching=teaching if teaching is not None else self.teaching_mode
        )
    
    def _service_scan(self, target: str, teaching: bool = None) -> Dict[str, Any]:
        """Scan with service version detection"""
        return self._scan(
            target=target,
            flags="-sV -sC",
            teaching=teaching if teaching is not None else self.teaching_mode
        )
    
    def _explain_scan(self, target: str, flags: str) -> Dict[str, Any]:
        """Explain what the scan will do"""
        explanations = {
            "-sV": "Service version detection - identifies service versions on open ports",
            "-sC": "Default scripts - runs default NSE scripts",
            "-sS": "TCP SYN scan - stealth scan, doesn't complete TCP handshake",
            "-sT": "TCP connect scan - completes full TCP connection",
            "-sU": "UDP scan - scans UDP ports (slower)",
            "-p": "Port specification - which ports to scan",
            "-A": "Aggressive scan - OS detection, version detection, scripts, traceroute",
            "-T4": "Timing template - faster execution (0-5, 4 is aggressive)",
            "-F": "Fast mode - scans fewer ports than default",
            "-Pn": "Skip ping - treat host as up even if it doesn't respond to ping",
            "-n": "No DNS resolution - faster but less information",
            "-O": "OS detection - attempts to identify operating system",
            "--script": "NSE script - runs specific Nmap Scripting Engine scripts"
        }
        
        flag_list = flags.split()
        explained_flags = []
        
        for flag in flag_list:
            flag_base = flag.split('=')[0].split(' ')[0]
            explained_flags.append({
                "flag": flag,
                "explanation": explanations.get(flag_base, "See nmap documentation")
            })
        
        return {
            "target": target,
            "flags": flags,
            "explained_flags": explained_flags,
            "scan_type": self._identify_scan_type(flags),
            "estimated_time": self._estimate_time(flags),
            "detectability": self._assess_detectability(flags),
            "recommendations": self._get_recommendations(flags)
        }
    
    def _identify_scan_type(self, flags: str) -> str:
        """Identify the type of scan"""
        if "-sV" in flags:
            return "Service Version Detection"
        elif "-sS" in flags:
            return "TCP SYN Stealth Scan"
        elif "-sU" in flags:
            return "UDP Scan"
        elif "-A" in flags:
            return "Aggressive Scan (OS + Version + Scripts)"
        else:
            return "Basic Scan"
    
    def _estimate_time(self, flags: str) -> str:
        """Estimate scan time"""
        if "-F" in flags or "-T4" in flags or "-T5" in flags:
            return "Fast (minutes)"
        elif "-A" in flags or "-sC" in flags:
            return "Medium (10-30 minutes)"
        elif "-sU" in flags:
            return "Slow (30+ minutes)"
        else:
            return "Medium (5-15 minutes)"
    
    def _assess_detectability(self, flags: str) -> str:
        """Assess how detectable the scan is"""
        if "-sS" in flags:
            return "Low (stealth scan)"
        elif "-A" in flags or "-sV" in flags:
            return "High (active probing)"
        else:
            return "Medium"
    
    def _get_recommendations(self, flags: str) -> List[str]:
        """Get recommendations for the scan"""
        recommendations = []
        
        if "-A" not in flags and "-sV" not in flags:
            recommendations.append("Add -sV for service version detection")
        
        if "-T" not in flags:
            recommendations.append("Consider -T4 for faster scanning")
        
        if "-Pn" not in flags:
            recommendations.append("Add -Pn if host blocks ping")
        
        recommendations.append("Always get written authorization before scanning")
        
        return recommendations
    
    def _get_learning_points(self, flags: str) -> List[str]:
        """Get learning points for this scan"""
        points = [
            "Nmap is the de facto standard for network scanning",
            "Always scan responsibly and with authorization",
            "Different scan types have different stealth levels",
            "Service version detection helps identify vulnerabilities"
        ]
        
        if "-sS" in flags:
            points.append("SYN scans don't complete TCP handshake (stealth)")
        
        if "-sV" in flags:
            points.append("Version detection may trigger IDS/IPS alerts")
        
        return points
    
    def _parse_output(self, output: str) -> Dict[str, Any]:
        """Parse nmap output"""
        parsed = {
            "hosts": [],
            "open_ports": [],
            "services": []
        }
        
        # Simple parsing (could be enhanced with XML output)
        lines = output.split('\n')
        current_host = None
        
        for line in lines:
            if 'Nmap scan report for' in line:
                current_host = line.split('for ')[-1].strip()
                parsed["hosts"].append(current_host)
            elif '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 2:
                    port_info = {
                        "port": parts[0],
                        "state": parts[1],
                        "service": parts[2] if len(parts) > 2 else "unknown"
                    }
                    parsed["open_ports"].append(port_info)
                    if parts[1] == "open":
                        parsed["services"].append(port_info)
        
        return parsed
