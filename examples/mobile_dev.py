#!/usr/bin/env python3
"""
Example: Mobile App Development

Demonstrates creating mobile apps for Android and iOS.
"""
import asyncio
from jarvis.core.orchestrator import Orchestrator


async def mobile_dev_demo():
    """Demo mobile development capabilities"""
    
    print("📱 Jarvis AI - Mobile App Development Demo")
    print("="*60)
    
    # Initialize
    jarvis = Orchestrator()
    await jarvis.start()
    jarvis.enable_teaching_mode()
    
    print("\n🎓 Teaching mode enabled - I'll explain everything!")
    
    # Check setup
    print(f"\n{'='*60}")
    print("Step 1: Check Development Setup")
    print('='*60)
    
    result = await jarvis.process_command("check mobile development setup")
    
    if result.get('success'):
        print("\n✓ Setup check complete!")
        if 'setup_status' in result:
            status = result['setup_status']
            print("\n   Available frameworks:")
            for framework, available in status.items():
                icon = "✓" if available else "✗"
                print(f"     {icon} {framework}")
        
        if 'explanation' in result and 'missing' in result['explanation']:
            missing = result['explanation']['missing']
            if missing:
                print(f"\n   ⚠️  Missing: {', '.join(missing)}")
                print("   Install them to use those frameworks")
    
    # Explain frameworks
    print(f"\n{'='*60}")
    print("Step 2: Understanding Mobile Frameworks")
    print('='*60)
    
    result = await jarvis.process_command("explain mobile development frameworks")
    
    if result.get('success') and 'explanation' in result:
        exp = result['explanation']
        if 'frameworks' in exp:
            print("\n📚 Framework Comparison:")
            for name, details in exp['frameworks'].items():
                print(f"\n   {name}:")
                print(f"     {details['description']}")
                if 'pros' in details:
                    print(f"     Pros: {', '.join(details['pros'][:2])}")
    
    # Example: Create React Native app
    print(f"\n{'='*60}")
    print("Step 3: Creating a React Native App")
    print('='*60)
    
    print("\n💡 Example command:")
    print("   'create a React Native app called DemoApp'")
    print("\n   This would:")
    print("   • Initialize new React Native project")
    print("   • Set up both Android and iOS support")
    print("   • Install dependencies")
    print("   • Provide next steps and learning resources")
    
    # Example: Create Flutter app
    print(f"\n{'='*60}")
    print("Step 4: Creating a Flutter App")
    print('='*60)
    
    print("\n💡 Example command:")
    print("   'create a Flutter app called MyFlutterApp'")
    print("\n   This would:")
    print("   • Initialize new Flutter project")
    print("   • Configure for Android and iOS")
    print("   • Explain Flutter concepts")
    print("   • Show how to build and run")
    
    # Framework comparison
    print(f"\n{'='*60}")
    print("Step 5: Choosing a Framework")
    print('='*60)
    
    result = await jarvis.process_command("explain how to choose mobile framework")
    
    if result.get('success') and 'explanation' in result:
        exp = result['explanation']
        if 'choosing' in exp:
            print("\n🤔 Decision Guide:")
            choosing = exp['choosing']
            
            if 'use_react_native' in choosing:
                print("\n   Choose React Native if you:")
                for reason in choosing['use_react_native'][:3]:
                    print(f"     • {reason}")
            
            if 'use_flutter' in choosing:
                print("\n   Choose Flutter if you:")
                for reason in choosing['use_flutter'][:3]:
                    print(f"     • {reason}")
    
    # Complete workflow example
    print(f"\n{'='*60}")
    print("Complete Workflow Example")
    print('='*60)
    
    print("""
To create a complete mobile app project:

1. Create GitHub repository:
   > create a GitHub repository called my-mobile-app

2. Create the mobile app:
   > create a React Native app called my-mobile-app
   OR
   > create a Flutter app called my-mobile-app

3. Navigate to project:
   > cd my-mobile-app

4. Make your changes and test

5. Commit your work:
   > commit changes with message "Initial app version"

6. Push to GitHub:
   > push to GitHub

7. Build for release:
   > build the app for Android
   > build the app for iOS

All with detailed explanations in teaching mode! 🎓
""")
    
    await jarvis.stop()
    print("\n✅ Mobile development demo complete!")
    print("\nNext steps:")
    print("  1. Install required tools (React Native, Flutter, etc.)")
    print("  2. Try creating your first app")
    print("  3. Enable teaching mode for guidance")
    print("  4. Build and deploy your app!")


if __name__ == "__main__":
    asyncio.run(mobile_dev_demo())
