from typing import Optional
from pydantic import BaseModel


# 接收到的消息格式
class Message(BaseModel):
    userid:str
    serviceid: str
    messages: list
    answer: Optional[str] = None

# 待润色的消息格式
class MessageWeak(BaseModel):
    userid:str
    serviceid: str
    message:str

