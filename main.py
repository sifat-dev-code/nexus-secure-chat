from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
import models
from database import engine
from routers import auth_routes, chat_routes
from auth import get_current_user

models.Base.metadata.create_all(bind=engine)
app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Shob origin allow korchi testing-er jonno
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, shob methods allow
    allow_headers=["*"],  # Shob headers allow
)
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)






@app.post("/create_room")
def create_room(name: str, username: str, db: Session = Depends(get_db)):
    # Database e notun ghor toiri
    new_room = models.Room(name=name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    room_creator = db.query(models.User).filter(models.User.username == username).first()
    if room_creator:
        new_member = models.RoomMember(room_id=new_room.id, user_id=room_creator.id)
        db.add(new_member)
        db.commit()
    return {"message": "Room created!", "room_id": new_room.id, "room_name": new_room.name}

@app.post("/add_member")
def add_member(room_id:int, username:str, db: Session = Depends(get_db)):
    new_member = db.query(models.User).filter(models.User.username==username).first()
    if new_member:
        added_member = models.RoomMember(room_id=room_id, user_id = new_member.id)
        db.add(added_member)
        db.commit()
        return {"message": "New member added successfully!"}
    
@app.get("/room/{room_id}/messages")
def chat_recover(room_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        # 1. Smart ID Extractor: current_user je format-ei thakuk, amra ashol ID ber kore nibo
        user_id = None
        if hasattr(current_user, "id"):
            user_id = current_user.id  # Jodi object hoy
        elif isinstance(current_user, dict):
            user_id = current_user.get("id") # Jodi dictionary hoy
        elif isinstance(current_user, int):
            user_id = current_user # Jodi direct integer ID hoy
        elif isinstance(current_user, str):
            # Jodi string/username hoy
            db_user = db.query(models.User).filter(models.User.username == current_user).first()
            if db_user:
                user_id = db_user.id

        if user_id is None:
            raise Exception(f"Developer Error: current_user theke ID ber kora jacche na. Data ashche erokom: {current_user}")

        # 2. Member check guard
        is_member = db.query(models.RoomMember).filter(
            models.RoomMember.room_id == room_id,
            models.RoomMember.user_id == user_id
        ).first()

        if not is_member:
            raise HTTPException(status_code=403, detail="Access Denied: Tumi ei ghorer member na!")

        # 3. Message tule ana
        recover_chat = db.query(models.Message).filter(
            models.Message.room_id == room_id,
            models.Message.is_deleted == False
        ).all()

        chat_history = []
        for msg in recover_chat:
            find_user = db.query(models.User).filter(models.User.id == msg.user_id).first()
            
            # Orphan Message Guard: Jodi kono user delete hoye giye thake, tateo app crash korbe na!
            sender_name = find_user.username if find_user else "Unknown User"
            
            chat_history.append({"sender": sender_name, "message": msg.content, "msg_id": msg.id})

        return chat_history

    except HTTPException:
        # 401 ba 403 error ashole ashte dibo
        raise
    except Exception as e:
        # Kono ajob crash hole ebar direct Swagger-e print hobe!
        raise HTTPException(status_code=500, detail=f"Server Crash Details: {str(e)}")