from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_rooms: dict[int, dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, client_id: str):
        await websocket.accept()
      
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = {}
        self.active_rooms[room_id][client_id]=websocket

    def disconnect(self, websocket: WebSocket, room_id: int, client_id : str):
        
        if room_id in self.active_rooms:
            if client_id in self.active_rooms[room_id]:
                del self.active_rooms[room_id][client_id]
            
            if not self.active_rooms[room_id]:
                del self.active_rooms[room_id]

    async def broadcast(self, message: dict, room_id: int):
        
        if room_id in self.active_rooms:
            disconnected_clients = []
            
            for c_id, connection in self.active_rooms[room_id].items():
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected_clients.append(c_id)
                    
        
            for dead_id in disconnected_clients:
                del self.active_rooms[room_id][dead_id]