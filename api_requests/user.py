from database.requests import set_tokens, get_refresh_token
from settings.config import HOST
from aiogram.client.session import aiohttp
from yarl import URL
from database.requests import get_token, update_token, logout

url = URL.build(
    scheme='http',
    host=HOST,
)


def header(user):
    token = get_token(user)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    return headers


async def login(validated_data, user_id):
    data = {
        'email': validated_data.get('email'),
        'password': validated_data.get('password')
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url.with_path('/login/'), data=data)
        if response.status == 200:
            body = await response.json()
            set_tokens(body, user_id)
            return True
        else:
            return False


async def register(validated_data):
    data = {
        'email': validated_data.get('email'),
        'password1': validated_data.get('password1'),
        'password2': validated_data.get('password2'),
        'first_name': validated_data.get('first_name'),
        'last_name': validated_data.get('last_name')
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url.with_path('/registration/'), data=data)
        if response.status == 201:
            return True
        else:
            return False


async def send_refresh_token(user):
    async with aiohttp.ClientSession() as session:
        token = get_refresh_token(user)
        request = session.post(
            url=url.with_path('/api/token/refresh/'),
            data={"refresh": str(token)}
        )
        response = await request
        if response.status == 200:
            body = await response.json()
            update_token(body, user)
            return True
        else:
            logout(user)
            return False


async def profile(user):
    endpoint = url.with_path('/user-profile/get_profile/')
    async with aiohttp.ClientSession() as session:
        request = session.get(url=endpoint, headers=header(user))
        response = await request
        if response.status == 200:
            body = await response.json()
            return body
        if response.status == 401:
            if await send_refresh_token(user):
                request = session.get(url=endpoint, headers=header(user))
                response = await request
                body = await response.json()
                return body
            else:
                return False
