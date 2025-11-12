# Jarvis AI

A comprehensive, modular Jarvis-like AI system for automation, security testing, development, and learning on Kali Linux.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for different tasks (Supervisor, Coder, Tutor, Recon, Defender)
- **Kali Linux Tool Integration**: Native support for nmap, metasploit, and all Kali tools
- **GitHub Integration**: Create repos, manage projects, issues, and PRs directly
- **Teaching Mode**: Learn while you work - detailed explanations for every action
- **Live Execution Mode**: Run commands immediately with minimal confirmation
- **Auto-Repair System**: Automatically detect and fix issues
- **Policy-Based Security**: Fine-grained permission control and safety checks
- **Plugin System**: Extensible architecture for adding new capabilities
- **Memory System**: Short-term and long-term memory with vector storage
- **Audit Logging**: Complete audit trail of all actions
- **REST API**: Full-featured API for integration
- **Interactive CLI**: User-friendly command-line interface

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/tanishq950/Jarvis-ai-.git
cd Jarvis-ai-

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Copy and configure environment
cp .env.example .env

# Edit .env with your settings
# IMPORTANT: Add your GitHub token for GitHub integration
# Get token from: https://github.com/settings/tokens
nano .env
```

### GitHub Setup (Optional but Recommended)

```bash
# Set your GitHub credentials
export GITHUB_TOKEN="your_github_personal_access_token"
export GITHUB_USERNAME="your_username"

# Or add to .env file
echo "GITHUB_TOKEN=your_token_here" >> .env
echo "GITHUB_USERNAME=your_username" >> .env

# Install GitHub CLI (recommended)
# On Debian/Ubuntu/Kali:
sudo apt install gh

# Authenticate
gh auth login
```

### Running Jarvis

#### Interactive Chat Mode

```bash
# Basic mode
jarvis chat

# With teaching mode (explains everything)
jarvis chat --teach

# Live mode (executes immediately - use with caution!)
jarvis chat --live

# Safe mode (maximum confirmations)
jarvis chat --safe
```

#### API Server Mode

```bash
# Start the API server
jarvis serve

# Custom host and port
jarvis serve --host 0.0.0.0 --port 8080
```

#### Single Command Execution

```bash
# Execute a single command
jarvis execute "explain nmap"

# Execute in live mode
jarvis execute "scan localhost" --live
```

## 🎓 Teaching Mode

Enable teaching mode to learn while using Kali Linux tools:

```bash
# In chat mode
jarvis chat --teach

# Or enable during session
You > teach me
Jarvis: Teaching mode enabled. I'll explain everything I do!

# Now any command will include detailed explanations
You > nmap -sV target.com
Jarvis: [Provides detailed explanation of nmap, flags, scan types, etc.]
```

### What Teaching Mode Provides

- **Tool Explanations**: Detailed description of what each tool does
- **Flag Descriptions**: Explanation of command-line flags and options
- **Security Warnings**: Important safety and legal considerations
- **Best Practices**: Recommendations and tips
- **Learning Points**: Key concepts to understand
- **Examples**: Practical usage examples

## 🔧 Using Kali Linux Tools

Jarvis integrates seamlessly with all Kali Linux tools:

### Network Scanning

```bash
You > nmap -sV target.com
You > run quick scan on target.com
You > explain what nmap does
```

### Web Testing

```bash
You > nikto -h target.com
You > run sqlmap on target.com
You > gobuster dir -u http://target.com -w wordlist.txt
```

### Password Cracking

```bash
You > explain john the ripper
You > hashcat -m 0 -a 0 hash.txt wordlist.txt
```

### Exploitation

```bash
You > search exploit for apache
You > explain metasploit modules
```

### Information Gathering

```bash
You > whois example.com
You > dig example.com
You > theHarvester -d target.com -b google
```

## 🔐 Live Mode

Enable live mode for immediate execution (use responsibly):

```bash
# In chat
You > enable live mode
Jarvis: ⚠️  Enable live mode? Commands will execute immediately!
[Confirm: yes]

# Now commands execute without additional confirmation
You > ls -la
[Executes immediately]

# Disable when done
You > disable live mode
```

## 🏗️ Architecture

```
jarvis/
├── core/               # Core system components
│   ├── orchestrator.py # Main system coordinator
│   ├── policy_engine.py# Security policy enforcement
│   ├── agent_manager.py# Agent lifecycle management
│   ├── memory.py       # Memory systems
│   └── config.py       # Configuration management
├── agents/             # Specialized agents
│   ├── supervisor.py   # Approval and oversight
│   ├── codegen.py      # Code generation
│   ├── tutor.py        # Teaching and explanations
│   ├── recon.py        # Security reconnaissance
│   └── defender.py     # Security monitoring
├── plugins/            # Tool integrations
│   ├── shell_plugin.py # All Kali tools support
│   ├── nmap_plugin.py  # Nmap integration
│   ├── metasploit_plugin.py # Metasploit integration
│   └── git_plugin.py   # Git operations
├── ui/                 # User interfaces
│   ├── api.py          # REST API
│   └── cli.py          # Command-line interface
├── data/               # Data storage
│   ├── policies/       # Security policies
│   └── embeddings/     # Vector database
└── workflows/          # Workflow definitions
```

## 📖 Usage Examples

### Learning Security Tools

```bash
You > teach me about nmap
Jarvis: [Comprehensive explanation of nmap...]

You > show me examples of nmap scans
Jarvis: [Provides various scan examples with explanations...]

You > what's the difference between -sS and -sT?
Jarvis: [Explains TCP SYN vs TCP Connect scans...]
```

### Code Generation

```bash
You > generate a Python script to scan ports
Jarvis: [Generates code with explanation...]

You > explain this code to me
Jarvis: [Line-by-line explanation...]
```

### Security Monitoring

```bash
You > monitor system security
Jarvis: [Runs security checks and provides report...]

You > check for vulnerabilities
Jarvis: [Scans and reports findings...]
```

## 🛡️ Security & Safety

### Policy Engine

All actions go through policy checks:

- **Permission-based**: Fine-grained control over what can be executed
- **Rate Limiting**: Prevents abuse and accidental DoS
- **Audit Logging**: Complete trail of all actions
- **Confirmation Required**: High-risk actions require approval

### Authorization Required

**IMPORTANT**: Always get written authorization before:
- Network scanning
- Penetration testing
- Vulnerability assessment
- Any security testing

Configure authorized targets in `data/policies/allowed_targets.json`.

### Safety Features

- **Dry Run Mode**: Preview actions before execution
- **Sandbox Execution**: Isolated environment for risky operations
- **Command Blacklist**: Prevents dangerous commands
- **Path Restrictions**: Protects system directories

## 🔌 API Reference

### REST API Endpoints

```bash
# Get system status
GET /status

# Execute command
POST /command
{
  "command": "explain nmap",
  "context": {},
  "user_approved": false
}

# Enable teaching mode
POST /teaching-mode?enable=true

# Enable live mode (requires confirmation)
POST /live-mode
{
  "enable": true,
  "confirm": true
}

# List agents
GET /agents

# List plugins
GET /plugins

# Get conversation history
GET /history?limit=10
```

### API Documentation

Full API documentation available at `http://localhost:8000/docs` when server is running.

## ⚙️ Configuration

### Environment Variables

Key settings in `.env`:

```bash
# Execution modes
DRY_RUN_MODE=false
ENABLE_PENTEST_TOOLS=false  # Enable with caution
ENABLE_CODE_EXECUTION=true
ENABLE_NETWORK_TOOLS=false

# Security
DEFAULT_TRUST_LEVEL=low  # low, medium, high
ENABLE_AUDIT_LOG=true

# Features
ENABLE_VOICE=false
```

### Policy Configuration

Edit `jarvis/data/policies/policies.json` to customize:

- Permission requirements
- Rate limits
- Allowed/blocked commands
- File system restrictions

## 🤝 Contributing

Contributions welcome! Please:

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Respect security guidelines

## 📄 License

MIT License - see LICENSE file

## ⚠️ Legal Disclaimer

This tool is for authorized testing only. Unauthorized access to computer systems is illegal. Always:

- Get written permission before testing
- Stay within scope of authorization
- Follow responsible disclosure practices
- Respect privacy and data protection laws

The authors are not responsible for misuse of this software.

## 🎯 Roadmap

- [x] Core architecture and orchestrator
- [x] Policy engine and security layer
- [x] Multi-agent system
- [x] Kali Linux tool integration
- [x] Teaching mode
- [x] Live execution mode
- [x] REST API and CLI
- [ ] LLM integration (Llama, Mistral, etc.)
- [ ] Vector database and RAG pipeline
- [ ] Voice interface (Whisper, TTS)
- [ ] Web UI dashboard
- [ ] Advanced workflow engine
- [ ] Automated reporting
- [ ] Bug bounty assistant
- [ ] Fine-tuning on security data

## 📞 Support

For issues, questions, or contributions:

- GitHub Issues: https://github.com/tanishq950/Jarvis-ai-/issues
- Documentation: See `/docs` directory

---

**Remember**: With great power comes great responsibility. Use Jarvis AI ethically and legally! 🦸‍♂️

## 🐙 GitHub Integration

Jarvis can manage your GitHub repositories and projects!

### Create Repositories

```bash
You > create a GitHub repository called my-awesome-project
You > make it a private repo with description "My awesome project"
```

### Manage Projects

```bash
You > create a new project board for my-repo
You > create an issue in my-repo: "Add user authentication"
You > make a pull request for my feature branch
```

### Clone and Work

```bash
You > clone my-repo from GitHub
You > commit these changes with message "Add feature"
You > push changes to GitHub
```

### With Teaching Mode

```bash
You > teach me about GitHub
You > explain what a pull request is
You > show me how to create a repository

[Jarvis provides detailed explanations of GitHub concepts]
```

### GitHub Commands

| Command | Action |
|---------|--------|
| `create repo <name>` | Create new repository |
| `create project <name>` | Create project board |
| `create issue <title>` | Create new issue |
| `create pr <title>` | Create pull request |
| `list repos` | List your repositories |
| `clone <repo>` | Clone repository |
| `commit changes` | Commit current changes |
| `push to github` | Push commits |

### API Usage

```python
import requests

# Create a repository
response = requests.post('http://localhost:8000/plugins/github/execute', json={
    'action': 'create_repo',
    'name': 'my-new-repo',
    'description': 'Created via Jarvis AI',
    'private': False
})

print(response.json())
```


## 📱 Mobile App Development

Create Android and iOS apps with ease!

### Supported Frameworks

- **React Native**: JavaScript/React cross-platform apps
- **Flutter**: Dart-based beautiful native apps
- **Native Android**: Kotlin/Java for Android-specific apps
- **Native iOS**: Swift/SwiftUI for iOS-specific apps

### Create Mobile Apps

```bash
# React Native (cross-platform)
You > create a React Native app called AwesomeApp
You > run the app on Android
You > build for iOS

# Flutter (cross-platform)
You > create a Flutter app called MyFlutterApp  
You > run on Android emulator
You > build APK for release

# Native development
You > teach me about native Android development
You > teach me about iOS with SwiftUI
```

### Complete Mobile Project Workflow

```bash
# Start with teaching mode
jarvis chat --teach

# 1. Check your setup
You > check mobile development setup

# 2. Create GitHub repo
You > create a GitHub repository called mobile-game

# 3. Create the app
You > create a React Native app called mobile-game

# 4. Develop (make your changes)

# 5. Commit and push
You > commit changes with message "Add game logic"
You > push to GitHub

# 6. Build for release
You > build the app for Android
You > build the app for iOS
```

### Framework Comparison

| Feature | React Native | Flutter | Native |
|---------|-------------|---------|---------|
| Language | JavaScript | Dart | Kotlin/Swift |
| Performance | Good | Excellent | Best |
| UI | Platform | Custom | Platform |
| Learning Curve | Easy (if know React) | Medium | Steep |
| Code Reuse | High | Very High | None |
| Community | Large | Growing | Huge |

### With Teaching Mode

```bash
You > teach me about mobile development
[Explains platforms, approaches, frameworks]

You > explain React Native vs Flutter
[Detailed comparison with pros/cons]

You > show me how to create an Android app
[Step-by-step guide with explanations]

You > explain mobile app architecture
[Teaches best practices and patterns]
```

### Mobile Dev Commands

| Command | Action |
|---------|--------|
| `create <framework> app <name>` | Create new app |
| `check mobile setup` | Verify tools installed |
| `run app on android` | Run on Android |
| `run app on ios` | Run on iOS |
| `build for android` | Build Android APK |
| `build for ios` | Build iOS IPA |
| `explain <framework>` | Learn about framework |


## 🔍 Bug Hunting & Vulnerability Scanning

Find security bugs automatically when you add an app link!

### Automated Vulnerability Detection

```bash
# Quick security scan
You > quick scan https://example.com

# Comprehensive bug hunt
You > find bugs in https://example.com

# With teaching mode - explains everything
You > teach me
You > scan for bugs in https://mywebsite.com
```

### Supported Scan Types

#### 1. Comprehensive Scan
Full security assessment with multiple tools:
- Port scanning (Nmap)
- Web vulnerability scanning (Nikto)
- SQL injection testing (SQLMap)
- Directory enumeration (Dirb)
- SSL/TLS security check
- Security header analysis

```bash
You > find bugs in https://target.com
You > comprehensive scan of https://app.example.com
You > security scan https://website.com
```

#### 2. Quick Scan
Fast security check for rapid assessment:
- Open ports and services
- Common web vulnerabilities
- Basic security issues

```bash
You > quick scan https://example.com
You > fast security check on https://target.com
```

#### 3. Specific Vulnerability Tests

**SQL Injection:**
```bash
You > test sql injection on https://site.com/page?id=1
You > check for sql vulnerabilities in https://app.com/login
```

**Cross-Site Scripting (XSS):**
```bash
You > test xss on https://example.com
You > check for xss vulnerabilities
```

**SSL/TLS Security:**
```bash
You > check ssl for example.com
You > verify ssl certificate of website.com
```

**Directory Enumeration:**
```bash
You > scan directories on https://example.com
You > find hidden files on website.com
```

**WordPress Security:**
```bash
You > scan wordpress site https://blog.example.com
You > check wordpress security
```

### Vulnerability Types Detected

| Vulnerability | Severity | Impact |
|--------------|----------|---------|
| SQL Injection | Critical | Database compromise |
| XSS (Cross-Site Scripting) | High | Session hijacking |
| Broken Authentication | High | Account takeover |
| Sensitive Data Exposure | High | Data breach |
| XML External Entities | High | Server compromise |
| Broken Access Control | High | Unauthorized access |
| Security Misconfiguration | Medium | System weakness |
| Insecure Deserialization | High | Remote code execution |
| Known Vulnerabilities | Varies | Depends on CVE |
| Insufficient Logging | Low | Missed attacks |

### Complete Bug Hunting Workflow

```bash
# Start with teaching mode
jarvis chat --teach

# 1. Get authorization (REQUIRED!)
You > I have permission to test https://myapp.com

# 2. Quick reconnaissance
You > quick scan https://myapp.com

# 3. Comprehensive analysis
You > find bugs in https://myapp.com

# 4. Specific tests based on findings
You > test sql injection on https://myapp.com/api/users?id=1
You > test xss on https://myapp.com/search
You > check ssl for myapp.com

# 5. Generate report
You > generate bug hunting report

# Every step includes detailed explanations!
```

### With Teaching Mode

```bash
You > teach me about bug hunting
[Explains methodology, OWASP Top 10, tools]

You > explain sql injection
[Details: how it works, impact, prevention]

You > explain owasp top 10
[Lists and explains common vulnerabilities]

You > what is xss
[Teaches about cross-site scripting]
```

### API Security Testing

```bash
You > scan api https://api.example.com
You > test api authentication
You > check api rate limiting
```

### Mobile App Security

```bash
You > scan android app /path/to/app.apk
You > analyze ios app security
```

### Bug Hunting Commands

| Command | Action |
|---------|--------|
| `find bugs in <url>` | Comprehensive scan |
| `quick scan <url>` | Fast assessment |
| `test sql injection on <url>` | SQL injection test |
| `test xss on <url>` | XSS vulnerability test |
| `check ssl for <domain>` | SSL/TLS security |
| `scan directories on <url>` | Find hidden files |
| `scan wordpress site <url>` | WordPress security |
| `scan api <url>` | API security test |
| `generate bug hunting report` | Create report |

### Tools Integrated

- **Nmap**: Network scanning & service detection
- **Nikto**: Web server vulnerability scanner
- **SQLMap**: Automated SQL injection testing
- **Dirb**: Directory & file enumeration
- **WPScan**: WordPress vulnerability scanner
- **OpenSSL**: SSL/TLS security analysis
- **Nuclei**: Template-based scanning
- **Custom Scripts**: Additional security checks

### Security Report Generation

```bash
You > generate bug hunting report
[Creates detailed report with:]
- Executive summary
- Vulnerability details
- Severity ratings
- Remediation steps
- Technical information
```

### OWASP Top 10 Coverage

✅ A1: Injection (SQL, NoSQL, OS command)
✅ A2: Broken Authentication  
✅ A3: Sensitive Data Exposure
✅ A4: XML External Entities (XXE)
✅ A5: Broken Access Control
✅ A6: Security Misconfiguration
✅ A7: Cross-Site Scripting (XSS)
✅ A8: Insecure Deserialization
✅ A9: Using Components with Known Vulnerabilities
✅ A10: Insufficient Logging & Monitoring

### Legal & Ethical Usage

⚠️ **IMPORTANT - READ CAREFULLY:**

**LEGAL REQUIREMENTS:**
- ✅ Always get **written permission** before scanning
- ✅ Only scan systems you own or are authorized to test
- ✅ Follow responsible disclosure practices
- ❌ Unauthorized scanning is **ILLEGAL**
- ❌ Never use for malicious purposes

**AUTHORIZATION:**
```bash
# Before any scan, confirm authorization
You > I have written permission to test https://target.com
Jarvis: ✓ Authorization noted. Proceeding with scan...
```

**RESPONSIBLE DISCLOSURE:**
1. Find vulnerability responsibly
2. Document findings clearly
3. Report to organization privately
4. Give time to fix (90 days typical)
5. Public disclosure only after fix

### Real-World Examples

**Example 1: Testing Your Website**
```bash
You > teach me
You > I own https://mywebsite.com
You > find bugs in https://mywebsite.com
[Jarvis performs comprehensive scan]
You > generate report
[Get detailed security assessment]
```

**Example 2: Bug Bounty Program**
```bash
You > I'm authorized for https://bugbounty.com
You > quick scan https://bugbounty.com
You > test sql injection on https://bugbounty.com/api?id=1
[If vulnerable, follow responsible disclosure]
```

**Example 3: Learning Security**
```bash
You > teach me about bug hunting
You > explain how sql injection works
You > show me xss examples
You > what are owasp top 10 vulnerabilities
```

### Features

- 🔍 Automated vulnerability scanning
- 🎓 Teaching mode explains everything
- 📊 Detailed security reports
- ⚡ Quick and comprehensive scans
- 🛡️ OWASP Top 10 coverage
- 🔧 Multiple security tools
- 📱 Mobile app testing
- 🌐 API security testing
- ⚠️ Legal safety warnings


## 💰 Stock Market Investment Advisory

Get intelligent stock market recommendations based on your investment amount!

### Investment Made Simple

```bash
# Just tell Jarvis your budget
You > I want to invest 500 rupees
You > invest 1000 rupees in short term
You > I have 5000 rupees for long term investment
```

### Short-term (Intraday) Trading

**When you say "short term" or "intraday":**
- Buy in **morning** (9:30 AM - 11:00 AM)
- Sell by **evening** (2:00 PM - 3:15 PM)
- Same-day trading (no overnight holding)
- 1-3% expected daily returns
- Higher risk, requires monitoring

```bash
You > I want to invest 500 rupees in short term

Jarvis: 📊 Short-term (Intraday) Recommendation
        
        Amount: ₹500
        
        Recommended Stock:
        • TATAMOTORS (₹720)
          BUY: 9:30 AM - 10:00 AM at ₹715
          SELL: 2:30 PM - 3:15 PM at ₹735
          Expected Return: 2-3%
          Stop Loss: ₹705
        
        [Teaching mode explains everything!]
```

### Long-term Investment

**When you say "long term":**
- Hold for 1-5+ years
- 12-18% annual returns
- Lower risk, minimal monitoring
- Get dividends
- Wealth creation

```bash
You > I want to invest 1000 rupees long term

Jarvis: 📈 Long-term Investment Recommendation
        
        Amount: ₹1000
        
        Recommended Stocks:
        • ITC (₹420) - 2 shares
          Expected: 15-20% per year
          Dividend: 3.8%
          Why: High dividend stock, diversified
        
        Investment Strategy:
        • Use SIP (monthly investing)
        • Review quarterly
        • Don't panic sell
        
        [Complete educational guidance!]
```

### Trading Timing Advice

**Intraday Best Times:**

| Time | Action | Description |
|------|--------|-------------|
| 9:30 AM - 10:00 AM | **BUY** | Morning stability |
| 10:00 AM - 11:00 AM | **BUY** | Best entry time |
| 12:00 PM - 1:00 PM | **SELL** | Mid-day profit booking |
| 2:00 PM - 3:15 PM | **SELL** | Pre-close exit |
| 3:15 PM | **MANDATORY EXIT** | Square off all positions |

**Avoid:**
- 9:15 AM - 9:30 AM (extreme volatility)
- 3:20 PM - 3:30 PM (closing rush)

### Investment Strategies Compared

| Feature | Short-term (Intraday) | Long-term |
|---------|----------------------|-----------|
| Holding | Same day | 1-5+ years |
| Risk | Very High | Low-Medium |
| Returns | 1-3% per day | 12-18% per year |
| Monitoring | Full-time | Quarterly |
| Suitable For | Experienced | Everyone |
| Stress Level | High | Low |

### With Teaching Mode

```bash
You > teach me
You > explain stock market basics
You > what is intraday trading
You > difference between short and long term
You > when should I buy stocks - morning or night

[Jarvis explains everything in detail!]
```

### Stock Market Commands

| Command | What It Does |
|---------|--------------|
| `invest 500 rupees` | Analyze investment options |
| `invest 1000 rupees short term` | Intraday recommendations |
| `invest 5000 rupees long term` | Long-term stocks |
| `intraday trading today` | Current intraday picks |
| `when to buy stocks` | Best timing advice |
| `when to sell intraday` | Exit timing |
| `teach me about stocks` | Educational content |

### Legal & Safe Data Sources

**We Use LEGAL Sources Only:**
✅ Yahoo Finance API (real-time prices)
✅ NSE/BSE Official Data (live market)
✅ Alpha Vantage (professional data)
✅ Public company filings
✅ Legitimate financial news

**We DO NOT Use:**
❌ Dark web (ILLEGAL & BLOCKED)
❌ Insider information (ILLEGAL)
❌ Unauthorized sources
❌ Manipulated data

All recommendations based on PUBLIC, LEGAL, REAL-TIME data!

### Example: Complete Investment Flow

```bash
# Start with teaching
jarvis chat --teach

# 1. Learn basics
You > teach me about stock market
[Jarvis explains concepts]

# 2. Get recommendations
You > I want to invest 1000 rupees short term
[Jarvis analyzes and recommends]

# 3. Understand timing
You > when should I buy this stock
[Jarvis: "Best time is 9:30 AM - 10:00 AM"]

# 4. Learn strategy
You > explain intraday trading strategy
[Complete educational content]

# 5. Make informed decision
[You decide based on education and data]
```

### ⚠️ Important Disclaimer

**This is for EDUCATIONAL PURPOSES ONLY:**
- NOT financial advice
- Consult SEBI-registered financial advisor
- Past performance ≠ future results
- You are responsible for decisions
- Markets involve risk - you can lose money

Always invest responsibly!

### Features

- 💰 Amount-based recommendations (₹500, ₹1000, etc.)
- ⏰ Buy/sell timing for intraday
- 📊 Short-term & long-term strategies
- 🎓 Teaching mode explains everything
- 📈 Real-time legal market data
- 🔒 Safe & compliant
- 📚 Investment education
- ⚖️ Legal data sources only

