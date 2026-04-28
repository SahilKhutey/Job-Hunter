from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from typing import List, Optional, Dict
import logging
from app.auth.jwt_handler import decode_token

logger = logging.getLogger(__name__)
router = APIRouter()

# ── Connection Manager (Elite Multi-User Isolation) ───────────────────────────
class ConnectionManager:
    def __init__(self):
        # Map user_id to a list of active WebSockets (one user can have multiple tabs)
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, ws: WebSocket, user_id: int):
        await ws.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(ws)
        logger.info(f"WS connected for User {user_id}. Active: {len(self.active_connections[user_id])}")

    def disconnect(self, ws: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if ws in self.active_connections[user_id]:
                self.active_connections[user_id].remove(ws)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"WS disconnected for User {user_id}.")

    async def broadcast(self, message: dict, user_id: Optional[int] = None):
        """
        Broadcast a JSON message. 
        If user_id is provided, only sends to that user's active sockets.
        """
        if user_id:
            targets = self.active_connections.get(user_id, [])
            dead = []
            for ws in targets:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.disconnect(ws, user_id)
        else:
            # Global broadcast (system alerts)
            for uid, connections in list(self.active_connections.items()):
                dead = []
                for ws in connections:
                    try:
                        await ws.send_json(message)
                    except Exception:
                        dead.append(ws)
                for ws in dead:
                    self.disconnect(ws, uid)

manager = ConnectionManager()

# ── Helper to emit from any service ──────────────────────────────────────────
async def emit_agent_update(agent: str, status: str, message: str, user_id: Optional[int] = None, strategic: bool = False):
    """Call this from any agent to push real-time updates. user_id is recommended."""
    await manager.broadcast({
        "type": "agent_update",
        "agent": agent,
        "status": status,
        "message": message,
        "strategic": strategic
    }, user_id=user_id)

async def emit_strategic_trace(agent: str, trace: str, user_id: Optional[int] = None):
    """Specific high-fidelity trace for strategic intelligence."""
    await manager.broadcast({
        "type": "agent_update",
        "agent": agent,
        "status": "strategic",
        "message": f"NEURAL_TRACE: {trace}",
        "strategic": True
    }, user_id=user_id)

async def emit_automation_step(step: str, status: str, agent: str = "Execution", user_id: Optional[int] = None):
    await manager.broadcast({
        "type": "automation",
        "step": step,
        "status": status,
        "agent": agent,
    }, user_id=user_id)

async def emit_browser_view(image_base64: str, user_id: Optional[int] = None):
    await manager.broadcast({
        "type": "browser_view",
        "image": image_base64,
    }, user_id=user_id)

# ── WebSocket Route with Security ─────────────────────────────────────────────
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = int(payload.get("sub", 0))
    await manager.connect(websocket, user_id)
    
    try:
        # Send a welcome ping
        await websocket.send_json({
            "type": "agent_update",
            "agent": "System",
            "status": "connected",
            "message": f"AI Job Hunter OS connected for User {user_id}. Mission Control ready.",
        })

        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WS Error (User {user_id}): {str(e)}")
        manager.disconnect(websocket, user_id)
