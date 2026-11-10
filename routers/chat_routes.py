from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Depends
from auth import SECRET_KEY, ALGORITHM
import jwt, models
from routers.chat_manager import ConnectionManager
from database import get_db
from sqlalchemy.orm import Session
router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id:str, token:str,room_id: int,db: Session = Depends(get_db)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    current_user = db.query(models.User).filter(models.User.username == client_id).first()
    is_member = db.query(models.RoomMember).filter(
            models.RoomMember.room_id == room_id,
            models.RoomMember.user_id == current_user.id
        ).first()
    if not is_member:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    await manager.connect(websocket, room_id, client_id)
    await manager.broadcast({"type": "presence", "sender": client_id, "status": "online"}, room_id)
    await manager.broadcast({"type": "status", "message": f"Client {client_id} joined the chat"}, room_id)
    try:
        while True:
            data: dict = await websocket.receive_json()
            if data.get("type") == "chat":              
                current_user = db.query(models.User).filter(models.User.username == client_id).first()            
                new_message = models.Message(content=data.get("message"), user_id=current_user.id, room_id=room_id)
                db.add(new_message)
                db.commit()
                db.refresh(new_message)
                await manager.broadcast({"type": "chat", "sender": client_id, "message": new_message.content, "msg_id": new_message.id}, room_id)
            elif data.get("type") == "unsend":
                target_id = data.get("msg_id")
                target_message = db.query(models.Message).filter(models.Message.id == target_id).first()
                if target_message and target_message.user_id == current_user.id:
                    target_message.is_deleted = True
                    db.commit()
                    await manager.broadcast({"type": "unsend", "msg_id": target_id}, room_id)
            elif data.get("type") == "typing":
                await manager.broadcast({"type": "typing", "sender": client_id}, room_id)
            elif data.get("type") == "screenshot":
                await manager.broadcast({"type": "screenshot", "sender": client_id}, room_id)
            elif data.get("type") == "theme":
                await manager.broadcast({
                    "type" : "theme",
                    "sender" : client_id,
                    "color" : data.get("color")
                }, room_id)
                

    except WebSocketDisconnect:
        if room_id in manager.active_rooms and client_id in manager.active_rooms[room_id]:
            manager.disconnect(websocket, room_id, client_id)
            await manager.broadcast({"type": "presence", "sender": client_id, "status": "offline"}, room_id)
            await manager.broadcast({"type": "status", "message": f"Client {client_id} left the chat"}, room_id)
