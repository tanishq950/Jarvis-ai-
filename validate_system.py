#!/usr/bin/env python3
"""
System Validation Script for Jarvis AI
Verifies all components are correctly installed and functional
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test all critical imports"""
    print("Testing module imports...")
    
    modules = {
        "Core": [
            "jarvis.core.orchestrator",
            "jarvis.core.policy_engine",
            "jarvis.core.agent_manager",
            "jarvis.core.memory",
            "jarvis.core.config",
            "jarvis.core.logger",
            "jarvis.core.auto_repair",
        ],
        "Agents": [
            "jarvis.agents.base",
            "jarvis.agents.supervisor",
            "jarvis.agents.codegen",
            "jarvis.agents.tutor",
            "jarvis.agents.recon",
            "jarvis.agents.defender",
        ],
        "Plugins": [
            "jarvis.plugins.base",
            "jarvis.plugins.plugin_manager",
            "jarvis.plugins.shell_plugin",
            "jarvis.plugins.nmap_plugin",
            "jarvis.plugins.metasploit_plugin",
            "jarvis.plugins.git_plugin",
            "jarvis.plugins.github_plugin",
            "jarvis.plugins.mobile_dev_plugin",
            "jarvis.plugins.bug_hunter_plugin",
            "jarvis.plugins.stock_market_plugin",
        ],
        "UI": [
            "jarvis.ui.api",
            "jarvis.cli",
        ],
    }
    
    all_success = True
    for category, module_list in modules.items():
        print(f"\n  {category}:")
        for module_name in module_list:
            try:
                __import__(module_name)
                print(f"    ✓ {module_name.split('.')[-1]}")
            except Exception as e:
                print(f"    ✗ {module_name.split('.')[-1]}: {str(e)[:60]}")
                all_success = False
    
    return all_success


def test_instantiation():
    """Test object creation"""
    print("\nTesting component instantiation...")
    
    try:
        from jarvis.core.orchestrator import Orchestrator
        orchestrator = Orchestrator()
        print("  ✓ Orchestrator created")
        
        status = orchestrator.get_status()
        print(f"  ✓ {len(status['agents'])} agents registered")
        print(f"  ✓ {len(status['plugins'])} plugins loaded")
        
        health = orchestrator.get_system_health()
        print(f"  ✓ System health: {health['status']}")
        
        return True, orchestrator
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_execution_modes(orchestrator):
    """Test execution modes"""
    print("\nTesting execution modes...")
    
    try:
        # Test live mode
        result = orchestrator.enable_live_mode(confirm=True)
        assert result['success'], "Live mode failed"
        print("  ✓ Live mode")
        
        # Test teaching mode
        result = orchestrator.enable_teaching_mode()
        assert result['success'], "Teaching mode failed"
        print("  ✓ Teaching mode")
        
        # Test auto-repair
        result = orchestrator.enable_auto_repair(confirm=True)
        assert result['success'], "Auto-repair failed"
        print("  ✓ Auto-repair mode")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_cli():
    """Test CLI"""
    print("\nTesting CLI...")
    
    try:
        from jarvis.cli import cli
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # Test version
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0, "Version command failed"
        print("  ✓ --version command")
        
        # Test status
        result = runner.invoke(cli, ['status'])
        assert result.exit_code == 0, "Status command failed"
        print("  ✓ status command")
        
        # Test agents
        result = runner.invoke(cli, ['agents'])
        assert result.exit_code == 0, "Agents command failed"
        print("  ✓ agents command")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_api():
    """Test API"""
    print("\nTesting API...")
    
    try:
        from jarvis.ui.api import app
        assert app.title == "Jarvis AI", "API title mismatch"
        print("  ✓ API app created")
        print(f"  ✓ API title: {app.title}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 70)
    print("JARVIS AI - SYSTEM VALIDATION")
    print("=" * 70)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test instantiation
    instantiation_ok, orchestrator = test_instantiation()
    
    # Test modes (only if orchestrator created)
    modes_ok = False
    if orchestrator:
        modes_ok = test_execution_modes(orchestrator)
    
    # Test CLI
    cli_ok = test_cli()
    
    # Test API
    api_ok = test_api()
    
    # Summary
    print("\n" + "=" * 70)
    results = {
        "Module imports": imports_ok,
        "Component instantiation": instantiation_ok,
        "Execution modes": modes_ok,
        "CLI interface": cli_ok,
        "API interface": api_ok,
    }
    
    all_passed = all(results.values())
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 70)
    
    if all_passed:
        print("✅ ALL VALIDATION TESTS PASSED!")
        print("\nJarvis AI is fully functional and ready to use!")
        print("\nQuick Start:")
        print("  • Interactive chat:  python -m jarvis.cli chat")
        print("  • With teaching:     python -m jarvis.cli chat --teach")
        print("  • With live mode:    python -m jarvis.cli chat --live")
        print("  • Start API server:  python -m jarvis.cli serve")
        return 0
    else:
        print("❌ SOME VALIDATION TESTS FAILED")
        print("\nPlease check the errors above and ensure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
