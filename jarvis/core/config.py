"""
Configuration management for Jarvis AI
"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Server Settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # LLM Settings
    llm_model_path: str = Field(default="models/llama-2-7b-chat.Q4_K_M.gguf", env="LLM_MODEL_PATH")
    llm_context_size: int = Field(default=4096, env="LLM_CONTEXT_SIZE")
    llm_max_tokens: int = Field(default=512, env="LLM_MAX_TOKENS")
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")
    
    # Memory Settings
    vector_db_path: str = Field(default="data/embeddings/chroma", env="VECTOR_DB_PATH")
    memory_db_path: str = Field(default="data/memory.db", env="MEMORY_DB_PATH")
    
    # Redis Settings
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # Security Settings
    session_secret_key: str = Field(default="your-secret-key-change-this", env="SESSION_SECRET_KEY")
    enable_audit_log: bool = Field(default=True, env="ENABLE_AUDIT_LOG")
    audit_log_path: str = Field(default="logs/audit.log", env="AUDIT_LOG_PATH")
    
    # Policy Settings
    policy_file: str = Field(default="data/policies/policies.json", env="POLICY_FILE")
    default_trust_level: str = Field(default="low", env="DEFAULT_TRUST_LEVEL")
    dry_run_mode: bool = Field(default=False, env="DRY_RUN_MODE")
    
    # Agent Settings
    max_concurrent_agents: int = Field(default=10, env="MAX_CONCURRENT_AGENTS")
    agent_timeout_seconds: int = Field(default=300, env="AGENT_TIMEOUT_SECONDS")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/jarvis.log", env="LOG_FILE")
    
    # Plugin Settings
    plugin_dir: str = Field(default="plugins", env="PLUGIN_DIR")
    enable_plugin_signing: bool = Field(default=False, env="ENABLE_PLUGIN_SIGNING")
    
    # Feature Flags
    enable_voice: bool = Field(default=False, env="ENABLE_VOICE")
    enable_pentest_tools: bool = Field(default=False, env="ENABLE_PENTEST_TOOLS")
    enable_code_execution: bool = Field(default=True, env="ENABLE_CODE_EXECUTION")
    enable_network_tools: bool = Field(default=False, env="ENABLE_NETWORK_TOOLS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
