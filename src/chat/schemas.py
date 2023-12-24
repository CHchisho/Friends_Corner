from pydantic import BaseModel


class MessagesModel(BaseModel):
    id: int
    id_sender: int
    id_recipient: int
    send_at: str
    message: str

    class Config:
        orm_mode = True

class MatchModel(BaseModel):
    id: int
    id_sender: int
    id_recipient: int
    answer: int