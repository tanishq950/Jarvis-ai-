"""
Plugin Manager - Manages all plugins and their lifecycle
"""
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base import PluginRegistry, JarvisPlugin
from ..core.logger import logger
from ..core.policy_engine import PolicyEngine

# Import available plugins
from .shell_plugin import ShellPlugin
from .nmap_plugin import NmapPlugin
from .metasploit_plugin import MetasploitPlugin
from .git_plugin import GitPlugin
from .github_plugin import GitHubPlugin
from .mobile_dev_plugin import MobileDevPlugin
from .bug_hunter_plugin import BugHunterPlugin
from .stock_market_plugin import StockMarketPlugin


class PluginManager:
    """
    Manages plugin lifecycle, registration, and teaching mode.
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        self.policy_engine = policy_engine
        self.registry = PluginRegistry()
        self.teaching_mode_enabled = False
        self._initialize_plugins()
    
    def _initialize_plugins(self):
        """Initialize and register all available plugins"""
        plugins = [
            ShellPlugin(),
            NmapPlugin(),
            MetasploitPlugin(),
            GitPlugin(),
            GitHubPlugin(),
            MobileDevPlugin(),
            BugHunterPlugin(),
            StockMarketPlugin()
        ]
        
        for plugin in plugins:
            try:
                # Register plugin
                if self.registry.register(plugin):
                    # Setup plugin with context
                    context = {
                        "policy_engine": self.policy_engine,
                        "teaching_mode": self.teaching_mode_enabled
                    }
                    
                    if plugin.setup(context):
                        logger.info(f"Plugin {plugin.manifest.name} setup successful")
                    else:
                        logger.warning(f"Plugin {plugin.manifest.name} setup failed")
            except Exception as e:
                logger.error(f"Error initializing plugin: {e}")
    
    def enable_teaching_mode(self):
        """Enable teaching mode for all plugins"""
        self.teaching_mode_enabled = True
        
        for plugin_name in self.registry.list_plugins():
            plugin = self.registry.get_plugin(plugin_name)
            if plugin and hasattr(plugin, 'enable_teaching_mode'):
                plugin.enable_teaching_mode()
                logger.info(f"Teaching mode enabled for plugin: {plugin_name}")
        
        logger.info("🎓 Teaching mode enabled globally")
        return {
            "success": True,
            "message": "Teaching mode enabled. All commands will include explanations.",
            "enabled_plugins": self.registry.list_plugins()
        }
    
    def disable_teaching_mode(self):
        """Disable teaching mode for all plugins"""
        self.teaching_mode_enabled = False
        
        for plugin_name in self.registry.list_plugins():
            plugin = self.registry.get_plugin(plugin_name)
            if plugin and hasattr(plugin, 'disable_teaching_mode'):
                plugin.disable_teaching_mode()
                logger.info(f"Teaching mode disabled for plugin: {plugin_name}")
        
        logger.info("Teaching mode disabled globally")
        return {
            "success": True,
            "message": "Teaching mode disabled."
        }
    
    def execute_plugin_action(
        self,
        plugin_name: str,
        action: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute an action on a specific plugin.
        
        Args:
            plugin_name: Name of the plugin
            action: Action to execute
            **kwargs: Action parameters
        
        Returns:
            Execution results
        """
        plugin = self.registry.get_plugin(plugin_name)
        
        if not plugin:
            return {
                "success": False,
                "error": f"Plugin not found: {plugin_name}",
                "available_plugins": self.registry.list_plugins()
            }
        
        if not plugin.enabled:
            return {
                "success": False,
                "error": f"Plugin not enabled: {plugin_name}"
            }
        
        # Check permissions
        for permission in plugin.get_permissions():
            policy_result = self.policy_engine.check_policy(
                action=permission,
                resource=f"{plugin_name}.{action}",
                metadata=kwargs
            )
            
            # Log the policy check
            logger.info(f"Policy check for {permission}: {policy_result}")
        
        # Execute the action
        try:
            result = plugin.execute(action, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Plugin execution error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_plugin(self, name: str) -> Optional[JarvisPlugin]:
        """Get a plugin by name"""
        return self.registry.get_plugin(name)
    
    def list_plugins(self) -> List[str]:
        """List all registered plugins"""
        return self.registry.list_plugins()
    
    def get_plugin_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get information about a plugin"""
        plugin = self.registry.get_plugin(name)
        
        if not plugin or not plugin.manifest:
            return None
        
        return {
            "name": plugin.manifest.name,
            "version": plugin.manifest.version,
            "description": plugin.manifest.description,
            "capabilities": [cap.value for cap in plugin.manifest.capabilities],
            "permissions": plugin.manifest.permissions,
            "enabled": plugin.enabled,
            "teaching_mode": getattr(plugin, 'teaching_mode', False)
        }
    
    def get_all_plugin_info(self) -> Dict[str, Any]:
        """Get information about all plugins"""
        info = {}
        for plugin_name in self.registry.list_plugins():
            plugin_info = self.get_plugin_info(plugin_name)
            if plugin_info:
                info[plugin_name] = plugin_info
        return info
