from database.requests import set_token
from settings.config import API
from aiogram.client.session import aiohttp
from database import users


async def login(validated_data, user_id):
    data = {
        'email': validated_data.get('email'),
        'password': validated_data.get('password')
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=API + 'login/', data=data)
        if response.status == 200:
            body = await response.json()
            await set_token(body, user_id)
            return True
        else:
            return False


async def register(validated_data, user_id):
    data = {
        'email': validated_data.get('email'),
        'password1': validated_data.get('password1'),
        'password2': validated_data.get('password2'),
        'first_name': validated_data.get('first_name'),
        'last_name': validated_data.get('last_name')
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=API + 'registration/', data=data)
        body = await response.json()
        print(body)
        return True
