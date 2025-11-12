"""
Logging configuration for Jarvis AI
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from pythonjsonlogger import jsonlogger


class AuditLogger:
    """Specialized logger for audit trails"""
    
    def __init__(self, log_path: str = "logs/audit.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("jarvis.audit")
        self.logger.setLevel(logging.INFO)
        
        # File handler with JSON format
        handler = logging.FileHandler(self.log_path)
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s %(user)s %(action)s %(resource)s %(result)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_action(
        self,
        action: str,
        resource: str,
        result: str,
        user: str = "system",
        metadata: Dict[str, Any] = None
    ):
        """Log an action to the audit log"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user,
            "action": action,
            "resource": resource,
            "result": result,
            "metadata": metadata or {}
        }
        self.logger.info(
            "Action performed",
            extra=log_entry
        )


def setup_logging(log_level: str = "INFO", log_file: str = "logs/jarvis.log"):
    """Setup logging configuration"""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Root logger
    logger = logging.getLogger("jarvis")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(console_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Global logger instances
logger = setup_logging()
audit_logger = AuditLogger()
