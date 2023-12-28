from datetime import datetime
from typing import List
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request
from pydantic import BaseModel

from auth.base_config import auth_backend, fastapi_users
from auth.models import User
from sqlalchemy import insert, select, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from chat.models import Messages, Match
from chat.schemas import MessagesModel, MatchModel
from auth.models import User
from auth.schemas import UserRead
from database import async_session_maker, get_async_session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
current_user = fastapi_users.current_user()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def send_personal_message(self, user_id_recipient: int, message: str, user_id_sender: int, websocket: WebSocket):
        await self.add_messages_to_database(user_id_recipient, message, user_id_sender)

        await websocket.send_text(str({"id_sender":str(user_id_sender),
                                         "id_recipient": str(user_id_recipient),
                                         "message": str(message)}))

    # async def broadcast(self, user_id_recipient: int, message: str, user_id_sender: int):
    #     await self.add_messages_to_database(user_id_recipient, message, user_id_sender)
    #
    #     for connection in self.active_connections:
    #         await connection.send_text(str({"id_sender":str(user_id_sender),
    #                                      "id_recipient": str(user_id_recipient),
    #                                      "message": str(message)}))










    @staticmethod
    async def add_messages_to_database(user_id_recipient: int, message: str, user_id_sender: int):
        now = datetime.now()
        async with async_session_maker() as session:
            stmt = insert(Messages).values(

                id_sender=user_id_sender,
                id_recipient=user_id_recipient,
                message=message,
                send_at=now.strftime("%m.%d.%Y, %H:%M:%S")
                # id_recipient=311,
                # message=message,
                # id_sender=211,
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()



@router.get("/approved_matches/{client_id}")
async def get_approved_matches(
        client_id: int,
        session: AsyncSession = Depends(get_async_session),
):

    query = select(Match).where(
        or_(
            Match.id_sender == client_id,
            Match.id_recipient == client_id
        ) & (Match.answer == 1)
    )
    match_data = await session.execute(query)
    match_data_list = [msg[0].as_dict() for msg in match_data.all()]

    # print(user_data_list)
    unique_recipients = set()
    for item in match_data_list:
        if any((elem['id_sender'] == item['id_recipient'] and elem['id_recipient'] == item['id_sender']) for elem in
               match_data_list):
            unique_recipients.add(item['id_recipient'])

    result_id = list(unique_recipients)
    # result_id.remove(client_id)

    query2 = select(User).where(User.id.in_(result_id)).order_by(User.id.desc())
    user_data = await session.execute(query2)
    user_data_list = [msg[0].as_dict() for msg in user_data.all()]


    return user_data_list


@router.get("/last_messages/{client_id}/{recipient_id}")
async def get_last_messages(
        client_id: int,
        recipient_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> List[MessagesModel]:
    # query = select(Messages).order_by(Messages.id.desc()).limit(10)
    query = select(Messages).where(
        (Messages.id_sender == client_id) &
        (Messages.id_recipient == recipient_id)
    ).order_by(Messages.send_at.desc()).offset(0).limit(20)
    messages = await session.execute(query)
    messages_list = [msg[0].as_dict() for msg in messages.all()]

    query2 = select(Messages).where(
        (Messages.id_sender == recipient_id) &
        (Messages.id_recipient == client_id)
    ).order_by(Messages.send_at.desc()).offset(0).limit(20)
    messages2 = await session.execute(query2)
    messages_list2 = [msg[0].as_dict() for msg in messages2.all()]
    messages_list.extend(messages_list2)

    def convert_to_datetime(item):
        # return datetime.strptime(item['send_at'], '%m.%d.%Y, %H:%M:%S')
        return item['id']
    sorted_data = sorted(messages_list, key=convert_to_datetime)
    # print(sorted_data[-20:])
    return sorted_data[-20:]
    # return messages.scalars().all()



@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int ):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            data = data.split('%%@%%')
            # print('\n      ', data, '\n')
            # await manager.broadcast(user_id_sender=client_id, user_id_recipient=int(data[0]), message=data[1])
            await manager.send_personal_message(user_id_sender=client_id, user_id_recipient=int(data[0]), message=data[1],websocket=websocket )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")






@router.get("/match/{client_id}")
async def get_match(
        client_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # query = select(Messages).order_by(Messages.id.desc()).limit(10)
    query = select(User).where(
        (User.id == client_id)
    )
    user_data = await session.execute(query)
    user_data_list = [msg[0].as_dict() for msg in user_data.all()]

    query2 = select(User).where(
        (User.gender == user_data_list[0]['friend_gender']) &
        (User.your_age <= user_data_list[0]['friend_age_to']) &
        (User.your_age >= user_data_list[0]['friend_age_from']) &
        (User.id != user_data_list[0]['id'])
    ).order_by(asc(User.id))
    user_data2 = await session.execute(query2)
    user_data_list2 = [msg[0].as_dict() for msg in user_data2.all()]

    query3 = select(Match).where(
        (Match.id_sender == user_data_list[0]['id'])
        # (Match.id_recipient == user_data_list2[0]['id'])
    )
    match_data = await session.execute(query3)
    match_data_list = [msg[0].as_dict()['id_recipient'] for msg in match_data.all()]

    id_to_delete = []
    for i in range(len(user_data_list2)):
        friend_id = user_data_list2[i]['id']
        # print(friend_id)
        if friend_id in match_data_list:
            id_to_delete.append(friend_id)

    # print('Your info:', user_data_list[0],'\n')
    # print('Find friend info:', user_data_list2,'\n')
    # print('Уже оцененные:', match_data_list)
    # user_data_list2 = [user_data for user_data in user_data_list2 if not(user_data['id'] in id_to_delete)]
    user_data_list3=[]
    for user_data in user_data_list2:
        if not(user_data['id'] in id_to_delete):
            for i in ['email','is_active','is_superuser', 'is_verified','friend_age_from','friend_age_to','friend_gender','hashed_password','phone_number','registered_at']:
                user_data.pop(i)
            user_data_list3.append(user_data)
    # print('Find friend new info:', '\n'.join(str(u) for u in user_data_list2),'\n')
    # print('Подходящие кандидаты: ', [us['id'] for us in user_data_list2])
    # print('Отправленные id: ', [us['id'] for us in user_data_list2][:5])
    return user_data_list3[:5]

class Answer(BaseModel):
    id_sender: int
    id_recipient: int
    answer: int
@router.post("/match")
async def post_match(answer: Answer):
    # print(answer)

    try:
        async with async_session_maker() as session:
            stmt = insert(Match).values(

                id_sender=answer.id_sender,
                id_recipient=answer.id_recipient,
                answer = answer.answer
            )
            await session.execute(stmt)
            await session.commit()
    finally:
        return {"status": 201}



