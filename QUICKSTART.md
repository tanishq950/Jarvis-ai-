# Jarvis AI - Quick Start Guide

Get up and running with Jarvis AI in minutes!

## Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/tanishq950/Jarvis-ai-.git
cd Jarvis-ai-

# Install dependencies
pip install -r requirements.txt

# Install Jarvis
pip install -e .
```

### 2. Configuration

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your preferences (optional)
nano .env
```

## Basic Usage

### Interactive Chat

```bash
# Start basic chat
jarvis chat

# Start with teaching mode
jarvis chat --teach

# Start with auto-repair
jarvis chat --auto-repair

# Start with live mode (careful!)
jarvis chat --live

# Combine modes
jarvis chat --teach --auto-repair
```

### API Server

```bash
# Start the API server
jarvis serve

# Custom port
jarvis serve --port 8080

# Access API docs at http://localhost:8000/docs
```

## Key Features

### 1. Teaching Mode 🎓

Learn while you work!

```bash
You > teach me
Jarvis: 🎓 Teaching mode enabled!

You > nmap -sV target.com
Jarvis: Let me explain...
        
        Tool: nmap (Network Mapper)
        Purpose: Network discovery and security auditing
        
        Flag -sV: Service version detection
        - Identifies versions of services on open ports
        - More intrusive than basic scan
        - May trigger IDS/IPS alerts
        
        Scan Type: Service Version Detection
        Estimated Time: Medium (5-15 minutes)
        Detectability: High (active probing)
        
        ⚠️  Always get written authorization before scanning!
```

### 2. Live Mode ⚡

Execute commands immediately:

```bash
You > enable live mode
Jarvis: ⚠️  Enable live mode? Commands will execute immediately!
[Confirm: yes]

You > ls -la
[Executes immediately without additional prompts]
```

### 3. Auto-Repair 🔧

Automatic problem fixing:

```bash
You > enable auto repair
Jarvis: 🔧 Auto-repair enabled!

You > import numpy
[Missing dependency detected]
Jarvis: Installing missing dependency: numpy
       [Automatically runs: pip install numpy]
       ✓ Successfully installed numpy
```

### 4. All Kali Tools 🛠️

Use any Kali Linux tool:

```bash
# Network scanning
You > nmap -sV target.com
You > masscan -p80,443 target.com

# Web testing
You > nikto -h target.com
You > sqlmap -u "http://target.com?id=1"
You > gobuster dir -u http://target.com -w /path/to/wordlist

# Password cracking
You > john --wordlist=/path/to/wordlist hash.txt
You > hashcat -m 0 -a 0 hash.txt wordlist.txt

# Exploitation
You > msfconsole
You > search exploit for apache

# Information gathering
You > whois example.com
You > dig example.com
You > theHarvester -d target.com -b google

# And many more...
```

## Common Commands

### In Chat Mode

```
help              - Show help
status            - System status
diagnostics       - Detailed diagnostics
teach me          - Enable teaching mode
enable live mode  - Enable live execution
enable auto repair- Enable auto-repair
exit              - Quit
```

### System Status

```bash
You > status
System Status:
  Running: True
  Mode: normal
  Live Mode: False
  Teaching Mode: True
  Auto-Repair: True
  Health: healthy
  Agents: supervisor, codegen, tutor, recon, defender
  Plugins: shell, nmap, metasploit, git
```

### Diagnostics

```bash
You > diagnose
System Diagnostics:
  Auto-Repair: Enabled
  Issues Detected: 3
  Unresolved: 0
  Repair Attempts: 3
  
  Recent Issues:
    ✓ [high] Missing Python dependency: numpy
    ✓ [medium] Configuration error
    ✓ [high] Tool not found: nmap
```

## Example Workflows

### Learning Session

```bash
jarvis chat --teach

You > teach me about nmap
[Get comprehensive explanation]

You > show me nmap examples
[See practical examples]

You > explain the difference between -sS and -sT
[Learn about scan types]

You > nmap -sV localhost
[See explanation + execute scan]
```

### Security Scanning

```bash
jarvis chat

You > scan target.com
[Requires authorization confirmation]

You > explain what was found
[Tutor agent explains results]

You > generate a report
[Creates markdown report]
```

### Code Generation

```bash
You > generate a Python script to scan ports
[Code generated with explanation]

You > explain this code to me
[Line-by-line walkthrough]

You > run the script
[Executes with safety checks]
```

## Safety Tips

### ⚠️ Important Reminders

1. **Authorization Required**: Always get written permission before scanning/testing
2. **Live Mode**: Use with extreme caution - commands execute immediately
3. **Auto-Repair**: Modifies your system - review what it does
4. **Teaching Mode**: Safe for learning, won't execute without confirmation

### Configuration

Edit `.env` to enable/disable features:

```bash
# Security
ENABLE_PENTEST_TOOLS=false  # Set to true to enable
ENABLE_NETWORK_TOOLS=false  # Set to true to enable
DEFAULT_TRUST_LEVEL=low     # low, medium, high

# Features
ENABLE_VOICE=false          # Voice interface (future)
```

### Target Authorization

Only scan authorized targets:

```bash
# Create allowed targets file
cp jarvis/data/policies/allowed_targets.json.example \
   jarvis/data/policies/allowed_targets.json

# Edit with your authorized targets
nano jarvis/data/policies/allowed_targets.json
```

## Troubleshooting

### Missing Dependencies

```bash
# Auto-repair will handle this, or manually:
pip install -r requirements.txt
```

### Tool Not Found

```bash
# Auto-repair will handle this, or manually on Kali:
sudo apt-get update
sudo apt-get install nmap metasploit-framework
```

### Permission Denied

```bash
# Some tools require elevated privileges
sudo jarvis chat

# Or use specific tools with sudo when needed
```

## Advanced Usage

### API Integration

```python
import requests

# Execute command
response = requests.post('http://localhost:8000/command', json={
    'command': 'explain nmap',
    'context': {},
    'user_approved': False
})

print(response.json())
```

### Custom Workflows

Create YAML workflows in `jarvis/workflows/`:

```yaml
name: my_workflow
description: Custom workflow
trigger: manual

steps:
  - agent: tutor
    task: "Explain the concept"
  - plugin: shell
    action: "run"
    params:
      command: "ls -la"
```

## Getting Help

```bash
# In chat
You > help

# Command line
jarvis --help
jarvis chat --help
jarvis serve --help

# Online
GitHub: https://github.com/tanishq950/Jarvis-ai-
Issues: https://github.com/tanishq950/Jarvis-ai-/issues
```

## Next Steps

1. ✅ Try basic commands
2. ✅ Enable teaching mode and learn
3. ✅ Explore Kali tools with explanations
4. ⏭️ Integrate LLM for advanced intelligence
5. ⏭️ Add voice interface
6. ⏭️ Build custom workflows
7. ⏭️ Contribute to the project!

---

**Remember**: Use responsibly and ethically! Always get proper authorization. 🦸‍♂️
