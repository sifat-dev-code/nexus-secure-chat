from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String, unique=True, index = True)
    password = Column(String)
class Room(Base):
    __tablename__= "rooms"
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, unique= True, index= True)
    
class Message(Base):
    __tablename__= "messages"
    id = Column(Integer, primary_key= True, index= True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    is_deleted = Column(Boolean, default=False)
class RoomMember(Base):
    __tablename__ = "room_members"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))