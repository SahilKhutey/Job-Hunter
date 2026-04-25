from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from typing import List, Optional
import logging
from app.auth.jwt_handler import decode_token

logger = logging.getLogger(__name__)
router = APIRouter()

# ── Connection Manager ─────────────────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        logger.info(f"WS connected. Total: {len(self.active)}")

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)
        logger.info(f"WS disconnected. Total: {len(self.active)}")

    async def broadcast(self, message: dict):
        """Broadcast a JSON message to all connected clients."""
        dead = []
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


# ── Helper to emit from any service ──────────────────────────────────────────
async def emit_agent_update(agent: str, status: str, message: str):
    """Call this from any agent to push real-time updates to the frontend."""
    await manager.broadcast({
        "type": "agent_update",
        "agent": agent,
        "status": status,
        "message": message,
    })


async def emit_automation_step(step: str, status: str):
    """Call this from the Playwright engine to stream automation steps."""
    await manager.broadcast({
        "type": "automation",
        "step": step,
        "status": status,
    })


async def emit_browser_view(image_base64: str):
    """Streams a live screenshot to the frontend."""
    await manager.broadcast({
        "type": "browser_view",
        "image": image_base64,
    })


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

    user_id = payload.get("sub")
    await manager.connect(websocket)
    
    try:
        # Send a welcome ping
        await websocket.send_json({
            "type": "agent_update",
            "agent": "System",
            "status": "connected",
            "message": f"AI Job Hunter OS connected for User {user_id}. Agents are online.",
        })

        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WS Error: {str(e)}")
        manager.disconnect(websocket)
