#!/usr/bin/env python3
"""
Example: GitHub Integration

Demonstrates GitHub operations with teaching mode.
"""
import asyncio
import os
from jarvis.core.orchestrator import Orchestrator


async def github_demo():
    """Demo GitHub integration capabilities"""
    
    print("🐙 Jarvis AI - GitHub Integration Demo")
    print("="*60)
    
    # Check for GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        print("\n⚠️  GITHUB_TOKEN not set!")
        print("   Get a token from: https://github.com/settings/tokens")
        print("   Then: export GITHUB_TOKEN='your_token_here'")
        return
    
    # Initialize
    jarvis = Orchestrator()
    await jarvis.start()
    jarvis.enable_teaching_mode()
    
    print("\n✓ Connected to GitHub")
    print(f"   User: {os.getenv('GITHUB_USERNAME', 'Not set')}")
    
    # Demo operations
    demos = [
        {
            "title": "List Repositories",
            "command": "list my GitHub repositories"
        },
        {
            "title": "Explain GitHub",
            "command": "explain GitHub basics"
        },
        {
            "title": "Create Repository (dry-run)",
            "command": "explain how to create a GitHub repository"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{'='*60}")
        print(f"Demo {i}: {demo['title']}")
        print('='*60)
        
        result = await jarvis.process_command(demo['command'])
        
        if result.get('success'):
            print(f"\n✓ Success!")
            
            if 'explanation' in result:
                exp = result['explanation']
                print(f"\n📖 Explanation:")
                if isinstance(exp, dict):
                    for key, value in exp.items():
                        if isinstance(value, list):
                            print(f"\n   {key}:")
                            for item in value:
                                print(f"     • {item}")
                        else:
                            print(f"   {key}: {value}")
                else:
                    print(f"   {exp}")
            
            if 'repositories' in result:
                print(f"\n   Found {result['count']} repositories:")
                for repo in result['repositories'][:5]:
                    print(f"     • {repo}")
        else:
            print(f"⚠️  {result.get('message', 'Action pending')}")
        
        print("\n" + "-"*60)
    
    # Example: Create a test repository (commented out for safety)
    print(f"\n{'='*60}")
    print("Example: Create Repository (not executed)")
    print('='*60)
    print("""
To create a repository, use:

    You > create a GitHub repository called test-project
    You > make it private with description "Test project"
    
Or programmatically:

    result = await jarvis.process_command(
        "create a GitHub repository called test-project"
    )
    
This will:
    1. Create the repository on GitHub
    2. Initialize with README if requested
    3. Provide detailed explanation of what was created
    4. Give you next steps and usage tips
""")
    
    await jarvis.stop()
    print("\n✅ GitHub demo complete!")


if __name__ == "__main__":
    asyncio.run(github_demo())
