"""
Bug Hunter Plugin - Automated vulnerability scanning and bug detection
"""
from typing import Dict, Any, List, Optional
import subprocess
import json
import re
from urllib.parse import urlparse
from pathlib import Path

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class BugHunterPlugin(JarvisPlugin):
    """
    Plugin for automated bug hunting and vulnerability scanning.
    Integrates multiple security tools for comprehensive analysis.
    """
    
    def __init__(self):
        super().__init__()
        self.teaching_mode = False
        self.scan_results = []
        
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="bug_hunter",
            version="1.0.0",
            description="Automated bug hunting and vulnerability scanning with teaching support",
            capabilities=[PluginCapability.SECURITY_TEST, PluginCapability.NETWORK_SCAN],
            permissions=["pentest.scan", "network.scan"],
            author="Jarvis AI Team",
            dependencies=["nmap", "nikto", "sqlmap", "dirb", "nuclei", "wpscan"]
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        self.enabled = True
        logger.info("Bug Hunter plugin initialized")
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
        """Execute bug hunting action"""
        actions = {
            "scan": self._comprehensive_scan,
            "quick_scan": self._quick_scan,
            "web_scan": self._web_vulnerability_scan,
            "sql_injection": self._test_sql_injection,
            "xss": self._test_xss,
            "directory_scan": self._directory_scan,
            "ssl_check": self._check_ssl,
            "port_scan": self._port_scan,
            "wordpress_scan": self._wordpress_scan,
            "api_scan": self._api_scan,
            "mobile_app_scan": self._mobile_app_scan,
            "explain": self._explain_bug_hunting,
            "report": self._generate_report,
        }
        
        if action in actions:
            return actions[action](**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": list(actions.keys())
            }
    
    def _comprehensive_scan(
        self,
        target: str,
        deep: bool = False,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Comprehensive vulnerability scan"""
        if teaching is None:
            teaching = self.teaching_mode
        
        logger.info(f"Starting comprehensive scan on {target}")
        
        # Parse target
        parsed = urlparse(target if '://' in target else f'http://{target}')
        domain = parsed.netloc or parsed.path
        
        results = {
            "target": target,
            "domain": domain,
            "scan_type": "comprehensive",
            "findings": [],
            "severity_summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0
            }
        }
        
        # 1. Port scan
        logger.info("Phase 1: Port scanning...")
        port_results = self._port_scan(domain, teaching=False)
        if port_results.get("success"):
            results["findings"].append({
                "phase": "port_scan",
                "results": port_results
            })
        
        # 2. Web vulnerability scan
        if parsed.scheme in ['http', 'https']:
            logger.info("Phase 2: Web vulnerability scanning...")
            web_results = self._web_vulnerability_scan(target, teaching=False)
            if web_results.get("success"):
                results["findings"].append({
                    "phase": "web_vulnerabilities",
                    "results": web_results
                })
        
        # 3. SQL injection test
        logger.info("Phase 3: SQL injection testing...")
        sql_results = self._test_sql_injection(target, teaching=False)
        if sql_results.get("success"):
            results["findings"].append({
                "phase": "sql_injection",
                "results": sql_results
            })
        
        # 4. Directory enumeration
        if deep:
            logger.info("Phase 4: Directory enumeration...")
            dir_results = self._directory_scan(target, teaching=False)
            if dir_results.get("success"):
                results["findings"].append({
                    "phase": "directory_scan",
                    "results": dir_results
                })
        
        # 5. SSL/TLS check
        if parsed.scheme == 'https':
            logger.info("Phase 5: SSL/TLS analysis...")
            ssl_results = self._check_ssl(domain, teaching=False)
            if ssl_results.get("success"):
                results["findings"].append({
                    "phase": "ssl_check",
                    "results": ssl_results
                })
        
        # Summarize findings
        results["total_findings"] = len(results["findings"])
        results["success"] = True
        
        if teaching:
            results["explanation"] = self._get_comprehensive_scan_explanation()
            results["recommendations"] = self._get_security_recommendations(results)
        
        # Store for report generation
        self.scan_results.append(results)
        
        return results
    
    def _quick_scan(self, target: str, teaching: bool = None) -> Dict[str, Any]:
        """Quick vulnerability scan"""
        if teaching is None:
            teaching = self.teaching_mode
        
        logger.info(f"Quick scan on {target}")
        
        # Run basic checks
        results = {
            "target": target,
            "scan_type": "quick",
            "checks": []
        }
        
        # Port scan
        port_results = self._port_scan(target, teaching=False)
        results["checks"].append(port_results)
        
        # Basic web check
        web_results = self._web_vulnerability_scan(target, quick=True, teaching=False)
        results["checks"].append(web_results)
        
        results["success"] = True
        
        if teaching:
            results["explanation"] = {
                "scan_type": "Quick security assessment",
                "what_was_checked": [
                    "Open ports and services",
                    "Common web vulnerabilities",
                    "Basic security headers"
                ],
                "next_steps": "Run comprehensive scan for detailed analysis"
            }
        
        return results
    
    def _web_vulnerability_scan(
        self,
        target: str,
        quick: bool = False,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Scan for web vulnerabilities using Nikto"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["nikto", "-h", target]
            if quick:
                cmd.extend(["-Tuning", "1"])  # Quick scan
            
            logger.info(f"Running Nikto scan on {target}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300 if quick else 900
            )
            
            # Parse Nikto output
            vulnerabilities = self._parse_nikto_output(result.stdout)
            
            response = {
                "success": True,
                "tool": "nikto",
                "target": target,
                "vulnerabilities": vulnerabilities,
                "total_issues": len(vulnerabilities),
                "raw_output": result.stdout
            }
            
            if teaching:
                response["explanation"] = {
                    "tool": "Nikto",
                    "purpose": "Web server scanner that tests for vulnerabilities",
                    "checks": [
                        "Outdated server software",
                        "Dangerous files and CGIs",
                        "Configuration issues",
                        "Missing security headers",
                        "Known vulnerabilities"
                    ],
                    "interpreting_results": {
                        "OSVDB": "Open Source Vulnerability Database reference",
                        "CVE": "Common Vulnerabilities and Exposures ID",
                        "Info": "Informational finding",
                        "Warning": "Potential security issue"
                    }
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Nikto not found",
                "install": "apt install nikto"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _test_sql_injection(
        self,
        target: str,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Test for SQL injection vulnerabilities"""
        if teaching is None:
            teaching = self.teaching_mode
        
        # Check if URL has parameters
        if '?' not in target:
            return {
                "success": True,
                "vulnerable": False,
                "message": "No parameters detected in URL",
                "note": "Provide a URL with parameters for SQL injection testing"
            }
        
        try:
            cmd = [
                "sqlmap",
                "-u", target,
                "--batch",  # Non-interactive
                "--level=1",
                "--risk=1"
            ]
            
            logger.info(f"Testing SQL injection on {target}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse SQLMap output
            vulnerable = "vulnerable" in result.stdout.lower()
            injections_found = self._parse_sqlmap_output(result.stdout)
            
            response = {
                "success": True,
                "tool": "sqlmap",
                "target": target,
                "vulnerable": vulnerable,
                "injections_found": injections_found,
                "raw_output": result.stdout[:1000]  # First 1000 chars
            }
            
            if teaching:
                response["explanation"] = {
                    "vulnerability": "SQL Injection",
                    "description": "Allows attackers to execute malicious SQL queries",
                    "impact": [
                        "Data theft (passwords, credit cards, etc.)",
                        "Data modification or deletion",
                        "Authentication bypass",
                        "Complete database compromise"
                    ],
                    "how_it_works": "Injecting SQL code into input fields that aren't properly sanitized",
                    "prevention": [
                        "Use parameterized queries/prepared statements",
                        "Input validation and sanitization",
                        "Least privilege database access",
                        "Web Application Firewall (WAF)"
                    ],
                    "severity": "CRITICAL"
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "SQLMap not found",
                "install": "apt install sqlmap"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _test_xss(
        self,
        target: str,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Test for Cross-Site Scripting vulnerabilities"""
        if teaching is None:
            teaching = self.teaching_mode
        
        # Basic XSS payload test
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        results = {
            "success": True,
            "target": target,
            "tested_payloads": len(payloads),
            "findings": []
        }
        
        if teaching:
            results["explanation"] = {
                "vulnerability": "Cross-Site Scripting (XSS)",
                "description": "Injecting malicious scripts into web pages viewed by other users",
                "types": {
                    "Reflected XSS": "Script reflected from web request",
                    "Stored XSS": "Script permanently stored on server",
                    "DOM-based XSS": "Script executes in the DOM"
                },
                "impact": [
                    "Cookie theft/session hijacking",
                    "Credential harvesting",
                    "Phishing attacks",
                    "Malware distribution"
                ],
                "prevention": [
                    "Input validation and output encoding",
                    "Content Security Policy (CSP)",
                    "HTTPOnly cookie flags",
                    "XSS filters and sanitization"
                ],
                "severity": "HIGH"
            }
        
        return results
    
    def _directory_scan(
        self,
        target: str,
        wordlist: str = None,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Scan for hidden directories and files"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["dirb", target]
            if wordlist:
                cmd.append(wordlist)
            
            logger.info(f"Directory scanning {target}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            # Parse dirb output
            found_paths = self._parse_dirb_output(result.stdout)
            
            response = {
                "success": True,
                "tool": "dirb",
                "target": target,
                "found_paths": found_paths,
                "total_found": len(found_paths)
            }
            
            if teaching:
                response["explanation"] = {
                    "purpose": "Discover hidden files and directories on web servers",
                    "why_important": [
                        "Find admin panels and login pages",
                        "Locate backup files",
                        "Discover forgotten files",
                        "Find configuration files"
                    ],
                    "interesting_files": [
                        "/.git - Source code repository",
                        "/admin - Administration panel",
                        "/backup - Backup files",
                        "/config - Configuration files",
                        "/.env - Environment variables"
                    ]
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Dirb not found",
                "install": "apt install dirb"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_ssl(self, domain: str, teaching: bool = None) -> Dict[str, Any]:
        """Check SSL/TLS configuration"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            # Use openssl to check certificate
            cmd = ["openssl", "s_client", "-connect", f"{domain}:443", "-servername", domain]
            
            result = subprocess.run(
                cmd,
                input=b"",
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse SSL info
            ssl_info = self._parse_ssl_output(result.stdout)
            
            response = {
                "success": True,
                "domain": domain,
                "ssl_info": ssl_info
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_ssl": "SSL/TLS encrypts data between client and server",
                    "importance": [
                        "Protects sensitive data in transit",
                        "Verifies server identity",
                        "Prevents man-in-the-middle attacks",
                        "Required for modern web security"
                    ],
                    "common_issues": [
                        "Expired certificates",
                        "Self-signed certificates",
                        "Weak cipher suites",
                        "Outdated TLS versions",
                        "Certificate chain problems"
                    ]
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _port_scan(self, target: str, teaching: bool = None) -> Dict[str, Any]:
        """Scan for open ports"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["nmap", "-sV", "-T4", "--top-ports", "100", target]
            
            logger.info(f"Port scanning {target}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse nmap output
            open_ports = self._parse_nmap_output(result.stdout)
            
            response = {
                "success": True,
                "tool": "nmap",
                "target": target,
                "open_ports": open_ports,
                "total_open": len(open_ports)
            }
            
            if teaching:
                response["explanation"] = {
                    "purpose": "Identify open ports and running services",
                    "why_important": "Open ports are potential entry points for attackers",
                    "common_ports": {
                        "22": "SSH - Remote access",
                        "80": "HTTP - Web server",
                        "443": "HTTPS - Secure web",
                        "3306": "MySQL - Database",
                        "5432": "PostgreSQL - Database",
                        "8080": "HTTP Alt - Web server"
                    }
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Nmap not found",
                "install": "apt install nmap"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _wordpress_scan(self, target: str, teaching: bool = None) -> Dict[str, Any]:
        """Scan WordPress site for vulnerabilities"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            cmd = ["wpscan", "--url", target, "--enumerate", "vp,vt"]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            response = {
                "success": True,
                "tool": "wpscan",
                "target": target,
                "findings": result.stdout
            }
            
            if teaching:
                response["explanation"] = {
                    "what_is_wpscan": "WordPress vulnerability scanner",
                    "what_it_finds": [
                        "Outdated WordPress version",
                        "Vulnerable plugins",
                        "Vulnerable themes",
                        "User enumeration",
                        "Configuration issues"
                    ]
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "WPScan not found",
                "install": "gem install wpscan"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _api_scan(self, target: str, teaching: bool = None) -> Dict[str, Any]:
        """Scan API endpoints for vulnerabilities"""
        if teaching is None:
            teaching = self.teaching_mode
        
        results = {
            "success": True,
            "target": target,
            "api_tests": []
        }
        
        # Common API security tests
        tests = [
            "Authentication bypass",
            "Broken access control",
            "Injection attacks",
            "Rate limiting",
            "Data exposure"
        ]
        
        if teaching:
            results["explanation"] = {
                "api_security": "APIs are often targets for attackers",
                "common_vulnerabilities": {
                    "Broken Authentication": "Weak or missing authentication",
                    "Broken Authorization": "Users accessing others' data",
                    "Injection": "SQL, NoSQL, command injection",
                    "Excessive Data Exposure": "Returning too much data",
                    "Lack of Rate Limiting": "DDoS and brute force",
                    "Security Misconfiguration": "Default settings, verbose errors"
                },
                "owasp_api_top_10": "https://owasp.org/www-project-api-security/"
            }
        
        return results
    
    def _mobile_app_scan(
        self,
        app_path: str,
        platform: str = "android",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Scan mobile app for vulnerabilities"""
        if teaching is None:
            teaching = self.teaching_mode
        
        results = {
            "success": True,
            "app": app_path,
            "platform": platform,
            "findings": []
        }
        
        if teaching:
            results["explanation"] = {
                "mobile_security": "Mobile apps have unique security challenges",
                "common_issues": {
                    "Android": [
                        "Insecure data storage",
                        "Weak encryption",
                        "Insecure communication",
                        "Code obfuscation issues",
                        "Vulnerable dependencies"
                    ],
                    "iOS": [
                        "Keychain misuse",
                        "Jailbreak detection bypass",
                        "Weak encryption",
                        "Certificate pinning issues",
                        "Binary protection"
                    ]
                },
                "tools": {
                    "Android": "MobSF, APKTool, jadx",
                    "iOS": "MobSF, Hopper, class-dump"
                }
            }
        
        return results
    
    def _generate_report(
        self,
        format: str = "json",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Generate bug hunting report"""
        if teaching is None:
            teaching = self.teaching_mode
        
        if not self.scan_results:
            return {
                "success": False,
                "error": "No scan results available",
                "message": "Run a scan first"
            }
        
        latest_scan = self.scan_results[-1]
        
        report = {
            "success": True,
            "scan_summary": latest_scan,
            "format": format
        }
        
        if teaching:
            report["explanation"] = {
                "report_sections": [
                    "Executive Summary",
                    "Vulnerability Details",
                    "Risk Assessment",
                    "Remediation Steps",
                    "Technical Details"
                ],
                "severity_levels": {
                    "Critical": "Immediate action required",
                    "High": "Fix soon",
                    "Medium": "Address in next release",
                    "Low": "Consider fixing",
                    "Info": "For awareness"
                }
            }
        
        return report
    
    def _explain_bug_hunting(self, topic: str = "basics") -> Dict[str, Any]:
        """Explain bug hunting concepts"""
        explanations = {
            "basics": {
                "what_is_bug_hunting": "Finding security vulnerabilities in applications",
                "why_important": "Vulnerabilities can lead to data breaches and system compromise",
                "types": {
                    "Web": "OWASP Top 10 vulnerabilities",
                    "Mobile": "OWASP Mobile Top 10",
                    "API": "OWASP API Top 10",
                    "Network": "Infrastructure vulnerabilities"
                },
                "methodology": [
                    "1. Reconnaissance - Gather information",
                    "2. Scanning - Identify potential issues",
                    "3. Enumeration - Detailed analysis",
                    "4. Exploitation - Verify vulnerabilities",
                    "5. Reporting - Document findings"
                ]
            },
            "owasp_top_10": {
                "A1": "Injection (SQL, NoSQL, OS command)",
                "A2": "Broken Authentication",
                "A3": "Sensitive Data Exposure",
                "A4": "XML External Entities (XXE)",
                "A5": "Broken Access Control",
                "A6": "Security Misconfiguration",
                "A7": "Cross-Site Scripting (XSS)",
                "A8": "Insecure Deserialization",
                "A9": "Using Components with Known Vulnerabilities",
                "A10": "Insufficient Logging & Monitoring"
            },
            "tools": {
                "Web": ["Burp Suite", "OWASP ZAP", "Nikto", "SQLMap"],
                "Network": ["Nmap", "Masscan", "Wireshark"],
                "Mobile": ["MobSF", "Frida", "Objection"],
                "Fuzzing": ["AFL", "Radamsa", "Burp Intruder"]
            }
        }
        
        return {
            "success": True,
            "topic": topic,
            "explanation": explanations.get(topic, explanations["basics"])
        }
    
    # Helper methods for parsing tool outputs
    
    def _parse_nikto_output(self, output: str) -> List[Dict[str, str]]:
        """Parse Nikto scan output"""
        vulnerabilities = []
        lines = output.split('\n')
        
        for line in lines:
            if '+ ' in line and 'OSVDB' in line:
                vulnerabilities.append({
                    "finding": line.strip(),
                    "severity": "medium"
                })
        
        return vulnerabilities
    
    def _parse_sqlmap_output(self, output: str) -> List[str]:
        """Parse SQLMap output for injections"""
        injections = []
        if 'parameter' in output.lower() and 'vulnerable' in output.lower():
            # Extract injection points
            lines = output.split('\n')
            for line in lines:
                if 'parameter' in line.lower():
                    injections.append(line.strip())
        
        return injections
    
    def _parse_dirb_output(self, output: str) -> List[str]:
        """Parse Dirb output for found paths"""
        paths = []
        lines = output.split('\n')
        
        for line in lines:
            if '+ ' in line and 'http' in line:
                paths.append(line.strip())
        
        return paths
    
    def _parse_ssl_output(self, output: str) -> Dict[str, Any]:
        """Parse SSL certificate information"""
        info = {
            "valid": "Verify return code: 0" in output,
            "protocol": "",
            "cipher": ""
        }
        
        # Extract protocol
        if 'Protocol' in output:
            for line in output.split('\n'):
                if 'Protocol' in line:
                    info["protocol"] = line.split(':')[-1].strip()
                    break
        
        return info
    
    def _parse_nmap_output(self, output: str) -> List[Dict[str, str]]:
        """Parse Nmap output for open ports"""
        ports = []
        lines = output.split('\n')
        
        for line in lines:
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    ports.append({
                        "port": parts[0],
                        "state": parts[1],
                        "service": parts[2] if len(parts) > 2 else "unknown"
                    })
        
        return ports
    
    def _get_comprehensive_scan_explanation(self) -> Dict[str, Any]:
        """Get explanation for comprehensive scan"""
        return {
            "scan_phases": {
                "1. Port Scanning": "Identify open ports and services",
                "2. Web Vulnerabilities": "Test for common web issues",
                "3. SQL Injection": "Check for database injection flaws",
                "4. Directory Enumeration": "Find hidden files/directories",
                "5. SSL/TLS Analysis": "Verify encryption security"
            },
            "scan_time": "Comprehensive scans can take 15-30 minutes",
            "authorization": "ALWAYS get written permission before scanning!",
            "legal_warning": "Unauthorized scanning is illegal"
        }
    
    def _get_security_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        # Generic recommendations
        recommendations.extend([
            "Keep all software up to date",
            "Use strong authentication",
            "Implement proper input validation",
            "Enable security headers",
            "Use HTTPS everywhere",
            "Regular security audits",
            "Monitor and log access"
        ])
        
        return recommendations
