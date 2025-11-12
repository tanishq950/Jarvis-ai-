"""
FastAPI REST API for Jarvis AI
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn

from ..core.orchestrator import Orchestrator
from ..core.config import settings
from ..core.logger import logger

# Create FastAPI app
app = FastAPI(
    title="Jarvis AI",
    description="A comprehensive Jarvis-like AI system",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator: Optional[Orchestrator] = None


# Request/Response models
class CommandRequest(BaseModel):
    command: str
    context: Optional[Dict[str, Any]] = None
    user_approved: bool = False


class CommandResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    message: Optional[str] = None


class LiveModeRequest(BaseModel):
    enable: bool
    confirm: bool = False


class ExecutionModeRequest(BaseModel):
    mode: str  # 'safe', 'normal', or 'live'


class AutoRepairRequest(BaseModel):
    enable: bool
    confirm: bool = False


class StatusResponse(BaseModel):
    running: bool
    execution_mode: str
    live_mode_enabled: bool
    teaching_mode_enabled: bool
    auto_repair_enabled: bool
    health_status: str
    agents: List[str]
    plugins: List[str]


# Startup/Shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize orchestrator on startup"""
    global orchestrator
    orchestrator = Orchestrator()
    await orchestrator.start()
    logger.info("Jarvis AI API server started")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global orchestrator
    if orchestrator:
        await orchestrator.stop()
    logger.info("Jarvis AI API server stopped")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Jarvis AI - Ready to assist",
        "version": "0.1.0",
        "status": "operational"
    }


@app.post("/auto-repair")
async def toggle_auto_repair(request: AutoRepairRequest):
    """
    Enable or disable automatic repair system.
    
    Auto-repair will automatically detect and fix common issues like:
    - Missing dependencies
    - Missing tools
    - Configuration errors
    - Permission issues
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    if request.enable:
        result = orchestrator.enable_auto_repair(confirm=request.confirm)
    else:
        result = orchestrator.disable_auto_repair()
    
    return result


@app.get("/health")
async def health_check():
    """Health check endpoint with detailed status"""
    if not orchestrator:
        return {
            "status": "unavailable",
            "running": False
        }
    
    health = orchestrator.get_system_health()
    
    return {
        "status": health["status"],
        "running": orchestrator.running,
        "details": health
    }


@app.get("/diagnostics")
async def get_diagnostics():
    """Get detailed system diagnostics"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    diagnostics = orchestrator.get_diagnostics()
    
    return {
        "success": True,
        "diagnostics": diagnostics
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "running": orchestrator.running if orchestrator else False
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    status = orchestrator.get_status()
    return StatusResponse(**status)


@app.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a command.
    
    This endpoint processes user commands and routes them to appropriate agents.
    In live mode, commands execute immediately with minimal confirmation.
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        result = await orchestrator.process_command(
            command=request.command,
            context=request.context,
            user_approved=request.user_approved
        )
        
        return CommandResponse(
            success=result.get("success", False),
            result=result,
            message=result.get("message")
        )
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/teaching-mode")
async def toggle_teaching_mode(enable: bool):
    """
    Enable or disable teaching mode.
    
    Teaching mode provides detailed explanations for every action,
    making it perfect for learning.
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    if enable:
        result = orchestrator.enable_teaching_mode()
    else:
        result = orchestrator.disable_teaching_mode()
    
    return result


@app.post("/live-mode")
async def toggle_live_mode(request: LiveModeRequest):
    """
    Enable or disable live mode.
    
    Live mode allows immediate execution with minimal confirmations.
    Use with caution!
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    if request.enable:
        result = orchestrator.enable_live_mode(confirm=request.confirm)
    else:
        result = orchestrator.disable_live_mode()
    
    return result


@app.post("/execution-mode")
async def set_execution_mode(request: ExecutionModeRequest):
    """
    Set execution mode.
    
    Modes:
    - safe: Maximum safety, confirms everything
    - normal: Policy-based confirmations
    - live: Minimal confirmations, immediate execution
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    result = orchestrator.set_execution_mode(request.mode)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.get("/plugins")
async def list_plugins():
    """List all available plugins"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    plugin_info = orchestrator.plugin_manager.get_all_plugin_info()
    
    return {
        "plugins": list(plugin_info.keys()),
        "plugin_details": plugin_info,
        "teaching_mode": orchestrator.teaching_mode_enabled
    }


@app.post("/plugins/{plugin_name}/execute")
async def execute_plugin(plugin_name: str, action: str, params: Optional[Dict[str, Any]] = None):
    """Execute a plugin action"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    params = params or {}
    
    result = orchestrator.plugin_manager.execute_plugin_action(
        plugin_name=plugin_name,
        action=action,
        **params
    )
    
    return result


@app.get("/agents")
async def list_agents():
    """List all available agents"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    agents = orchestrator.agent_manager.list_agents()
    capabilities = orchestrator.agent_manager.get_capabilities()
    
    return {
        "agents": agents,
        "capabilities": capabilities
    }


@app.get("/agents/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """Get status of a specific agent"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    status = orchestrator.agent_manager.get_agent_status(agent_name)
    
    if status is None:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_name}")
    
    return {
        "agent": agent_name,
        "status": status
    }


@app.get("/history")
async def get_history(limit: int = 10):
    """Get conversation history"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    history = orchestrator.get_conversation_history(limit)
    return {
        "history": history,
        "count": len(history)
    }


@app.get("/memory/events")
async def get_events(event_type: Optional[str] = None, limit: int = 50):
    """Get event timeline"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    events = orchestrator.memory.long_term.get_events(event_type, limit)
    return {
        "events": events,
        "count": len(events)
    }


@app.post("/memory/remember")
async def remember(key: str, value: Any, persist: bool = False):
    """Store information in memory"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    orchestrator.memory.remember(key, value, persist)
    return {
        "success": True,
        "message": f"Stored {key}",
        "persist": persist
    }


@app.get("/memory/recall/{key}")
async def recall(key: str):
    """Retrieve information from memory"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    value = orchestrator.memory.recall(key)
    
    if value is None:
        raise HTTPException(status_code=404, detail=f"Key not found: {key}")
    
    return {
        "key": key,
        "value": value
    }


def run_server(host: str = None, port: int = None):
    """Run the API server"""
    host = host or settings.host
    port = port or settings.port
    
    logger.info(f"Starting Jarvis AI server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()

@app.post("/bug-hunt/scan")
async def bug_hunt_scan(request: dict):
    """
    Run vulnerability scan on target
    
    Body:
    {
        "target": "https://example.com",
        "scan_type": "comprehensive|quick",
        "deep": false
    }
    """
    target = request.get("target")
    scan_type = request.get("scan_type", "quick")
    deep = request.get("deep", False)
    
    if not target:
        return {"error": "Target URL required"}
    
    plugin = orchestrator.plugin_manager.get_plugin("bug_hunter")
    if not plugin:
        return {"error": "Bug hunter plugin not available"}
    
    if scan_type == "comprehensive":
        result = plugin.execute("scan", target=target, deep=deep, teaching=True)
    else:
        result = plugin.execute("quick_scan", target=target, teaching=True)
    
    return result


@app.post("/bug-hunt/sql-injection")
async def test_sql_injection(request: dict):
    """
    Test for SQL injection vulnerabilities
    
    Body:
    {
        "target": "https://example.com/page?id=1"
    }
    """
    target = request.get("target")
    
    if not target:
        return {"error": "Target URL required"}
    
    plugin = orchestrator.plugin_manager.get_plugin("bug_hunter")
    if not plugin:
        return {"error": "Bug hunter plugin not available"}
    
    result = plugin.execute("sql_injection", target=target, teaching=True)
    return result


@app.post("/bug-hunt/xss")
async def test_xss(request: dict):
    """
    Test for XSS vulnerabilities
    
    Body:
    {
        "target": "https://example.com"
    }
    """
    target = request.get("target")
    
    if not target:
        return {"error": "Target URL required"}
    
    plugin = orchestrator.plugin_manager.get_plugin("bug_hunter")
    if not plugin:
        return {"error": "Bug hunter plugin not available"}
    
    result = plugin.execute("xss", target=target, teaching=True)
    return result


@app.get("/bug-hunt/report")
async def get_bug_hunt_report():
    """Get bug hunting report"""
    plugin = orchestrator.plugin_manager.get_plugin("bug_hunter")
    if not plugin:
        return {"error": "Bug hunter plugin not available"}
    
    result = plugin.execute("report", format="json", teaching=True)
    return result
