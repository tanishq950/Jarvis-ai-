"""
Base classes for Jarvis plugins
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum

from ..core.logger import logger, audit_logger


class PluginCapability(Enum):
    """Plugin capability types"""
    SYSTEM_COMMAND = "system.command"
    FILE_OPERATION = "file.operation"
    NETWORK_SCAN = "network.scan"
    CODE_GENERATION = "code.generation"
    DATA_ANALYSIS = "data.analysis"
    SECURITY_TEST = "security.test"


class PluginManifest:
    """Plugin metadata and requirements"""
    
    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        capabilities: List[PluginCapability],
        permissions: List[str],
        author: str = "Unknown",
        dependencies: Optional[List[str]] = None
    ):
        self.name = name
        self.version = version
        self.description = description
        self.capabilities = capabilities
        self.permissions = permissions
        self.author = author
        self.dependencies = dependencies or []


class JarvisPlugin(ABC):
    """
    Base class for all Jarvis plugins.
    Plugins extend Jarvis functionality with specific tools and capabilities.
    """
    
    def __init__(self):
        self.manifest: Optional[PluginManifest] = None
        self.context: Dict[str, Any] = {}
        self.enabled = False
    
    @abstractmethod
    def get_manifest(self) -> PluginManifest:
        """Return plugin manifest with metadata and requirements"""
        pass
    
    @abstractmethod
    def setup(self, context: Dict[str, Any]) -> bool:
        """
        Initialize the plugin with context.
        Returns True if setup successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def teardown(self) -> bool:
        """
        Clean up plugin resources.
        Returns True if teardown successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a plugin action.
        
        Args:
            action: Action identifier
            **kwargs: Action parameters
        
        Returns:
            Dict with execution results
        """
        pass
    
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities"""
        if self.manifest:
            return self.manifest.capabilities
        return []
    
    def get_permissions(self) -> List[str]:
        """Get list of required permissions"""
        if self.manifest:
            return self.manifest.permissions
        return []
    
    def log_action(self, action: str, result: str, metadata: Optional[Dict] = None):
        """Log plugin action to audit log"""
        audit_logger.log_action(
            action=f"plugin.{self.manifest.name}.{action}",
            resource=self.manifest.name,
            result=result,
            user="system",
            metadata=metadata or {}
        )


class PluginRegistry:
    """Registry for managing plugins"""
    
    def __init__(self):
        self.plugins: Dict[str, JarvisPlugin] = {}
        logger.info("Plugin registry initialized")
    
    def register(self, plugin: JarvisPlugin) -> bool:
        """Register a plugin"""
        try:
            manifest = plugin.get_manifest()
            if manifest.name in self.plugins:
                logger.warning(f"Plugin {manifest.name} already registered")
                return False
            
            self.plugins[manifest.name] = plugin
            plugin.manifest = manifest
            logger.info(f"Registered plugin: {manifest.name} v{manifest.version}")
            return True
        except Exception as e:
            logger.error(f"Error registering plugin: {e}")
            return False
    
    def unregister(self, name: str) -> bool:
        """Unregister a plugin"""
        if name in self.plugins:
            plugin = self.plugins[name]
            plugin.teardown()
            del self.plugins[name]
            logger.info(f"Unregistered plugin: {name}")
            return True
        return False
    
    def get_plugin(self, name: str) -> Optional[JarvisPlugin]:
        """Get a plugin by name"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[str]:
        """List all registered plugins"""
        return list(self.plugins.keys())
    
    def get_plugins_by_capability(self, capability: PluginCapability) -> List[JarvisPlugin]:
        """Get all plugins with a specific capability"""
        return [
            plugin for plugin in self.plugins.values()
            if capability in plugin.get_capabilities()
        ]
