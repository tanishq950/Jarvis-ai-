#!/usr/bin/env python3
"""
Example: Bug Hunting and Vulnerability Scanning

Demonstrates automated bug finding in web applications and APIs.
"""
import asyncio
from jarvis.core.orchestrator import Orchestrator


async def bug_hunting_demo():
    """Demo bug hunting capabilities"""
    
    print("🔍 Jarvis AI - Bug Hunter Demo")
    print("="*60)
    print("⚠️  LEGAL WARNING: Only scan systems you own or have")
    print("   explicit written permission to test!")
    print("="*60)
    
    # Initialize
    jarvis = Orchestrator()
    await jarvis.start()
    jarvis.enable_teaching_mode()
    
    print("\n🎓 Teaching mode enabled - I'll explain everything!")
    
    # Explain bug hunting
    print(f"\n{'='*60}")
    print("What is Bug Hunting?")
    print('='*60)
    
    result = await jarvis.process_command("explain bug hunting basics")
    
    if result.get('success') and 'explanation' in result:
        exp = result['explanation']
        if 'what_is_bug_hunting' in exp:
            print(f"\n📚 {exp['what_is_bug_hunting']}")
        
        if 'methodology' in exp:
            print("\n   Methodology:")
            for step in exp['methodology']:
                print(f"     {step}")
    
    # Explain OWASP Top 10
    print(f"\n{'='*60}")
    print("OWASP Top 10 Vulnerabilities")
    print('='*60)
    
    result = await jarvis.process_command("explain owasp top 10")
    
    if result.get('success') and 'explanation' in result:
        exp = result['explanation']
        print("\n   Most common web vulnerabilities:")
        for vuln, desc in list(exp.items())[:5]:
            print(f"     • {vuln}: {desc}")
        print("     ... and 5 more")
    
    # Example scans (demonstration only)
    print(f"\n{'='*60}")
    print("Bug Hunting Commands")
    print('='*60)
    
    examples = [
        {
            "title": "Quick Vulnerability Scan",
            "command": "quick scan https://example.com",
            "what_it_does": [
                "Port scanning",
                "Basic web vulnerability check",
                "Security headers analysis",
                "Quick assessment"
            ]
        },
        {
            "title": "Comprehensive Security Scan",
            "command": "find bugs in https://example.com",
            "what_it_does": [
                "Full port scan with service detection",
                "Web vulnerability scanning (Nikto)",
                "SQL injection testing (SQLMap)",
                "Directory enumeration",
                "SSL/TLS security check",
                "Detailed report generation"
            ]
        },
        {
            "title": "SQL Injection Test",
            "command": "test sql injection on https://example.com/page?id=1",
            "what_it_does": [
                "Tests URL parameters for SQL injection",
                "Identifies vulnerable parameters",
                "Determines database type",
                "Provides exploitation guidance"
            ]
        },
        {
            "title": "XSS Vulnerability Test",
            "command": "test xss on https://example.com",
            "what_it_does": [
                "Tests for cross-site scripting",
                "Tries multiple XSS payloads",
                "Identifies reflection points",
                "Explains XSS impact"
            ]
        },
        {
            "title": "WordPress Security Scan",
            "command": "scan wordpress site https://example.com",
            "what_it_does": [
                "Checks WordPress version",
                "Scans for vulnerable plugins",
                "Identifies vulnerable themes",
                "User enumeration",
                "Configuration issues"
            ]
        },
        {
            "title": "API Security Test",
            "command": "scan api https://api.example.com",
            "what_it_does": [
                "OWASP API Top 10 checks",
                "Authentication testing",
                "Authorization testing",
                "Rate limiting checks",
                "Data exposure analysis"
            ]
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   Command: '{example['command']}'")
        print(f"   What it does:")
        for item in example['what_it_does']:
            print(f"     • {item}")
    
    # Vulnerability explanations
    print(f"\n{'='*60}")
    print("Understanding Common Vulnerabilities")
    print('='*60)
    
    print("""
1. SQL Injection (Critical)
   - Allows attackers to execute malicious SQL queries
   - Can lead to complete database compromise
   - Prevention: Use parameterized queries

2. Cross-Site Scripting - XSS (High)
   - Inject malicious scripts into web pages
   - Steal cookies, session tokens, credentials
   - Prevention: Input validation & output encoding

3. Broken Authentication (High)
   - Weak password policies
   - Session management issues
   - Prevention: Strong auth mechanisms, MFA

4. Sensitive Data Exposure (High)
   - Unencrypted data transmission
   - Weak encryption algorithms
   - Prevention: Use TLS, strong encryption

5. Security Misconfiguration (Medium)
   - Default credentials
   - Unnecessary features enabled
   - Prevention: Secure configuration, hardening
""")
    
    # Complete workflow
    print(f"\n{'='*60}")
    print("Complete Bug Hunting Workflow")
    print('='*60)
    
    print("""
Step 1: Get Authorization
   > Obtain written permission to test the target

Step 2: Information Gathering
   > Quick scan https://target.com
   > Learn about target infrastructure

Step 3: Comprehensive Scanning
   > Find bugs in https://target.com
   > Wait for complete analysis

Step 4: Specific Vulnerability Tests
   > Test SQL injection on vulnerable endpoint
   > Test XSS on input fields
   > Check SSL security

Step 5: Generate Report
   > Generate bug hunting report
   > Document all findings with severity

Step 6: Responsible Disclosure
   > Report vulnerabilities to the organization
   > Follow responsible disclosure practices

All with teaching mode explaining each vulnerability! 🎓
""")
    
    # Tools overview
    print(f"\n{'='*60}")
    print("Bug Hunting Tools Integrated")
    print('='*60)
    
    tools = {
        "Nmap": "Network scanner & port detection",
        "Nikto": "Web server vulnerability scanner",
        "SQLMap": "Automated SQL injection tool",
        "Dirb": "Directory & file bruteforcer",
        "WPScan": "WordPress security scanner",
        "OpenSSL": "SSL/TLS security testing",
        "Burp Suite": "Web application security (manual)",
        "OWASP ZAP": "Web app security scanner"
    }
    
    print("\n   Available tools:")
    for tool, description in tools.items():
        print(f"     • {tool}: {description}")
    
    await jarvis.stop()
    print("\n✅ Bug hunting demo complete!")
    print("\n⚠️  REMEMBER:")
    print("   • Always get permission before scanning")
    print("   • Unauthorized testing is illegal")
    print("   • Follow responsible disclosure")
    print("   • Use for learning and authorized testing only")


if __name__ == "__main__":
    asyncio.run(bug_hunting_demo())
