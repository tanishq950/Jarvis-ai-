"""
Memory system for Jarvis AI
Handles short-term and long-term memory, vector storage, and knowledge base
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime
import sqlite3

from .logger import logger


class ShortTermMemory:
    """Ephemeral memory for current session"""
    
    def __init__(self):
        self.context: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []
        self.max_history = 100
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to conversation history"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.history.append(entry)
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_history(self, last_n: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        return self.history[-last_n:]
    
    def set_context(self, key: str, value: Any):
        """Set context variable"""
        self.context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context variable"""
        return self.context.get(key, default)
    
    def clear(self):
        """Clear all memory"""
        self.context = {}
        self.history = []


class LongTermMemory:
    """Persistent memory storage using SQLite"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    type TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    metadata TEXT,
                    UNIQUE(type, key)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_type_key 
                ON memories(type, key)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    metadata TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON events(timestamp)
            """)
    
    def store(self, memory_type: str, key: str, value: Any, metadata: Optional[Dict] = None):
        """Store a memory"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO memories 
                    (timestamp, type, key, value, metadata)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        datetime.utcnow().isoformat(),
                        memory_type,
                        key,
                        json.dumps(value),
                        json.dumps(metadata or {})
                    )
                )
        except Exception as e:
            logger.error(f"Error storing memory: {e}")
    
    def retrieve(self, memory_type: str, key: str) -> Optional[Any]:
        """Retrieve a memory"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT value FROM memories WHERE type = ? AND key = ?",
                    (memory_type, key)
                )
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
        return None
    
    def search(self, memory_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories by type"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT timestamp, key, value, metadata 
                    FROM memories 
                    WHERE type = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                    """,
                    (memory_type, limit)
                )
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "timestamp": row[0],
                        "key": row[1],
                        "value": json.loads(row[2]),
                        "metadata": json.loads(row[3])
                    })
                return results
        except Exception as e:
            logger.error(f"Error searching memories: {e}")
        return []
    
    def log_event(self, event_type: str, description: str, metadata: Optional[Dict] = None):
        """Log an event to the timeline"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO events (timestamp, event_type, description, metadata)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        datetime.utcnow().isoformat(),
                        event_type,
                        description,
                        json.dumps(metadata or {})
                    )
                )
        except Exception as e:
            logger.error(f"Error logging event: {e}")
    
    def get_events(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if event_type:
                    cursor = conn.execute(
                        """
                        SELECT timestamp, event_type, description, metadata 
                        FROM events 
                        WHERE event_type = ?
                        ORDER BY timestamp DESC 
                        LIMIT ?
                        """,
                        (event_type, limit)
                    )
                else:
                    cursor = conn.execute(
                        """
                        SELECT timestamp, event_type, description, metadata 
                        FROM events 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                        """,
                        (limit,)
                    )
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "timestamp": row[0],
                        "event_type": row[1],
                        "description": row[2],
                        "metadata": json.loads(row[3])
                    })
                return results
        except Exception as e:
            logger.error(f"Error retrieving events: {e}")
        return []


class MemoryManager:
    """Unified memory management"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(db_path)
        logger.info("Memory system initialized")
    
    def remember(self, key: str, value: Any, persist: bool = False, metadata: Optional[Dict] = None):
        """Store information in memory"""
        if persist:
            self.long_term.store("knowledge", key, value, metadata)
        else:
            self.short_term.set_context(key, value)
    
    def recall(self, key: str, check_long_term: bool = True) -> Optional[Any]:
        """Retrieve information from memory"""
        # Check short-term first
        value = self.short_term.get_context(key)
        if value is not None:
            return value
        
        # Check long-term if requested
        if check_long_term:
            return self.long_term.retrieve("knowledge", key)
        
        return None
