from pydantic import BaseModel



class Message(BaseModel):
    type: str
    sender: str
    new_message: str
    history_message: str = ""
    reply_message: str = ""




