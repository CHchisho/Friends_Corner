from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from typing import List
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request, FastAPI
from pydantic import BaseModel

from auth.base_config import auth_backend, fastapi_users
from auth.models import User
from sqlalchemy import insert, select, asc, or_, delete
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
                send_at=now.strftime("%Y.%m.%d, %H:%M:%S")
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

    # def convert_to_datetime(item):
    #     # return datetime.strptime(item['send_at'], '%m.%d.%Y, %H:%M:%S')
    #     return item['id']
    sorted_data = sorted(messages_list, key=lambda x: x["send_at"])
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


class Mesg(BaseModel):
    id_sender: int
    id_recipient: int
    message: str
@router.post("/ws_chat")
async def ws_chat(mesg: Mesg):
    try:
        now = datetime.now()
        async with async_session_maker() as session:
            stmt = insert(Messages).values(
                id_sender=mesg.id_sender,
                id_recipient=mesg.id_recipient,
                message=mesg.message,
                send_at=now.strftime("%Y.%m.%d, %H:%M:%S")
            )
            await session.execute(stmt)
            await session.commit()
    finally:
        return {'status': 201, 'data': {'id_sender': mesg.id_sender,
                                        'id_recipient': mesg.id_recipient,
                                        'message': mesg.message}}


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


@router.get("/all_data_from_database_for_admin")
async def all_data_from_database_for_admin(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    user_data = await session.execute(query)
    user_data_list = [msg[0].as_dict() for msg in user_data.all()]

    query2 = select(Match)
    user_data2 = await session.execute(query2)
    user_data_list2 = [msg[0].as_dict() for msg in user_data2.all()]

    query3 = select(Messages)
    user_data3 = await session.execute(query3)
    user_data_list3 = [msg[0].as_dict() for msg in user_data3.all()]
    return [user_data_list,user_data_list2,user_data_list3]

@router.get("/create_test_user_for_admin")
async def create_test_user_for_admin():
    async with async_session_maker() as session:
        stmt = insert(User).values(test_users_data)
        await session.execute(stmt)
        await session.commit()

    async with async_session_maker() as session:
        stmt2 = insert(Match).values(test_user_data_match)
        await session.execute(stmt2)
        await session.commit()

    async with async_session_maker() as session:
        stmt3 = insert(Messages).values(test_user_data_chat)
        await session.execute(stmt3)
        await session.commit()
    print("Test user data created!")
    return {"status": 200}

@router.get("/delete_test_user_for_admin")
async def delete_test_user_for_admin():

    async with async_session_maker() as session:
        id_to_keep = [50, 51, 52, 53, 54,55]

        stmt = delete(Match).where(
            (Match.id_sender == 70) & ~Match.id.in_(id_to_keep)
        )
        await session.execute(stmt)
        await session.commit()

    async with async_session_maker() as session:
        id_to_keep2 = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

        stmt2 = delete(Messages).where(
            (Messages.id_sender == 70) & ~Messages.id.in_(id_to_keep2)
        )
        await session.execute(stmt2)
        await session.commit()

    print("Test user data was deleted")
    return {"status": 200}

scheduler = AsyncIOScheduler()
async def job():
    id_to_keep = [50, 51, 52, 53, 54, 55]
    id_to_keep2 = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    async with async_session_maker() as session:
        stmt = delete(Match).where(
            (Match.id_sender == 70) & ~Match.id.in_(id_to_keep)
        )
        await session.execute(stmt)
        await session.commit()

    async with async_session_maker() as session:
        stmt2 = delete(Messages).where(
            (Messages.id_sender == 70) & ~Messages.id.in_(id_to_keep2)
        )
        await session.execute(stmt2)
        await session.commit()

    print("Test user data was deleted")
# Запускаем задачу каждые 30 секунд
scheduler.add_job(job, trigger=IntervalTrigger(hours=6))
scheduler.start()



test_users_data = [
    {'id': 70, 'email': 'amelia_test@gmail.com', 'username': 'Amelia', 'phone_number': '+358123456789', 'gender': 'girl',
     'regions': 'Satakunta', 'your_age': 18, 'hobbies': 'acting&collecting&gaming&board-games&flea-markets&graphic-design',
     'about_you': 'A globetrotter with a camera in hand. From capturing moments to trying new recipes, every day is an adventure.',
     'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 30, 'registered_at': datetime(2023, 12, 28, 17, 48, 59),
     'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True, 'is_superuser': False, 'is_verified': False},

    {'id': 71, 'email': 'jena_doe1@gmail.com', 'username': 'Jena', 'phone_number': '+123456789012', 'gender': 'girl',
     'regions': 'Ahvenanmaa', 'your_age': 25, 'hobbies': 'reading&photography&traveling&video-games&cooking&sports',
     'about_you': 'I am a passionate individual who loves exploring new things and meeting people. Always up for a good book or an exciting adventure!',
     'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 28, 'registered_at': datetime(2023, 11, 15, 10, 30, 45),
     'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True, 'is_superuser': False, 'is_verified': False},

    {'id': 72, 'email': 'alice_smith2@gmail.com', 'username': 'Alice', 'phone_number': '+441234567890', 'gender': 'girl',
    'regions': 'London', 'your_age': 22, 'hobbies': 'painting&music&dancing&movies&hiking&technology',
    'about_you': 'An artist at heart, I find inspiration in every corner of life. Music and dancing are my escape, and Im always up for a new painting project!',
    'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 25, 'registered_at': datetime(2023, 10, 5, 15, 20, 30),
    'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True, 'is_superuser': False, 'is_verified': False},

    {'id': 73, 'email': 'amelia_jones3@gmail.com', 'username': 'Amelia', 'phone_number': '+612345678901', 'gender': 'girl',
    'regions': 'Satakunta', 'your_age': 28, 'hobbies': 'surfing&coding&music-production&cooking&photography&sports',
    'about_you': 'A tech enthusiast with a love for the ocean. I spend my weekends coding and catching waves. Always looking for a new coding challenge!',
    'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 30, 'registered_at': datetime(2023, 9, 20, 8, 45, 15),
    'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True, 'is_superuser': False, 'is_verified': False},

    {'id': 74, 'email': 'sophie_wilson4@gmail.com', 'username': 'Sophie', 'phone_number': '+812345678901', 'gender': 'girl',
    'regions': 'Kymenlaakso', 'your_age': 23, 'hobbies': 'anime&manga&writing&traveling&art&cooking',
    'about_you': 'A creative soul with a passion for storytelling. Whether its through writing or art, I love expressing myself.Lets explore the world together!',
    'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 28, 'registered_at': datetime(2023, 8, 10, 12, 10,5),
    'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True, 'is_superuser': False, 'is_verified': False},

    {'id': 75, 'email': 'lidia_clark5@gmail.com', 'username': 'Lidia', 'phone_number': '+447890123456', 'gender': 'girl',
    'regions': 'Pirkanmaa', 'your_age': 19, 'hobbies': 'gardening&reading&photography&cooking&technology&movies',
    'about_you': 'A bookworm and tech enthusiast with a green thumb. You can find me either in the garden or immersed in the latest tech trends. Lets share our favorite books!',
    'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 35, 'registered_at': datetime(2023, 7, 5, 18, 30, 40),
    'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True,'is_superuser': False, 'is_verified': False},

    {'id': 76, 'email': 'emily_white6@gmail.com', 'username': 'Emily', 'phone_number': '+614567890123', 'gender': 'girl',
    'regions': 'Pohjanmaa', 'your_age': 26, 'hobbies': 'music&dancing&traveling&photography&painting&movies',
    'about_you': 'A coding enthusiast who loves the outdoors. Whether its writing code or exploring nature trails, I find joy in every moment.',
    'friend_gender': 'girl', 'friend_age_from': 15, 'friend_age_to': 30, 'registered_at': datetime(2023, 6, 18, 14, 15, 22),
    'hashed_password': '$2b$12$OlKYWpLnxlsnpMuWCxEbROo9KExkMVmnl0rPNPHLaEe7CaiKVaH.6', 'is_active': True, 'is_superuser': False, 'is_verified': False},


]

test_user_data_match = [
    {'id': 50, 'id_sender': 70, 'id_recipient': 71, 'answer': 1},
    {'id': 51, 'id_sender': 71, 'id_recipient': 70, 'answer': 1},
    {'id': 52, 'id_sender': 70, 'id_recipient': 72, 'answer': 1},
    {'id': 53, 'id_sender': 72, 'id_recipient': 70, 'answer': 1},

    {'id': 54, 'id_sender': 73, 'id_recipient': 70, 'answer': 1},
    {'id': 55, 'id_sender': 74, 'id_recipient': 70, 'answer': 1},
]

test_user_data_chat = [
    {'id': 50, 'id_sender': 73, 'id_recipient': 70, 'send_at': '2024.01.01, 11:21:01',
     'message': 'Hello, are you new?'},
    {'id': 51, 'id_sender': 74, 'id_recipient': 70, 'send_at': '2024.01.01, 16:41:21',
     'message': 'Hi, how are you?'},

    {'id': 52, 'id_sender': 70, 'id_recipient': 71, 'send_at': '2023.12.25, 10:15:00',
    'message': "Hey, how's it going?"},
    {'id': 53, 'id_sender': 71, 'id_recipient': 70, 'send_at': '2023.12.25, 10:17:12',
    'message': "Hi there! I'm doing well, thanks. How about you?"},
    {'id': 54, 'id_sender': 70, 'id_recipient': 71, 'send_at': '2023.12.25, 10:30:45',
    'message': 'Nice! What are your plans for the weekend?'},
    {'id': 55, 'id_sender': 71, 'id_recipient': 70, 'send_at': '2023.12.25, 10:32:18',
    'message': 'Not sure yet. Maybe catching up on some movies. Any recommendations?'},

    {'id': 56, 'id_sender': 70, 'id_recipient': 72, 'send_at': '2023.12.18, 11:00:00',
    'message': "Hey, how's your day going so far?"},
    {'id': 57, 'id_sender': 72, 'id_recipient': 70, 'send_at': '2023.12.18, 11:02:30',
    'message': "Hi! It's been a good day. How about yours?"},
    {'id': 58, 'id_sender': 70, 'id_recipient': 72, 'send_at': '2023.12.18, 11:15:45',
    'message': 'Awesome! Any exciting plans for the evening?'},
    {'id': 59, 'id_sender': 72, 'id_recipient': 70, 'send_at': '2023.12.18, 11:18:20',
    'message': 'Thinking of grabbing dinner with friends. How about you?'},
]
