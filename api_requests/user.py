from abc import ABC, abstractmethod
from httpx import Response
from database.requests import set_tokens, get_refresh_token
from settings.config import HOST
from aiogram.client.session import aiohttp
from yarl import URL
from database.requests import get_token, update_token, logout
import httpx


class BaseApiClient(ABC):

    def __init__(self, user):
        self.user = user
        self.url = URL.build(
            scheme='http',
            host=HOST,
        )

    @abstractmethod
    def handler_response_errors(self, response: Response) -> Response:
        pass

    @property
    def client(self):
        return httpx.Client()

    async def send_refresh_token(self, request):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=str(self.url.with_path('/api/token/refresh/')),
                data={"refresh": get_refresh_token(self.user)}
            )
            if response.status_code == 200:
                response_data = response.json()
                token = response_data.get('access')
                update_token(token, self.user)
                request.headers['Authorization'] = 'Bearer ' + token
                response = await client.send(request)
                return response
            else:
                logout(self.user)
                return response

    async def send_request(self, request):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.send(request)
                if response.status_code == 401:
                    response = await self.send_refresh_token(request)
            return response
        except Exception as error:
            raise error


class UserApiClient(BaseApiClient):

    def handler_response_errors(self, response: Response) -> Response:
        return response

    def get_header(self) -> dict:
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + get_token(self.user)
        }
        return headers

    async def register(self, validated_data):
        data = {
            'email': validated_data.get('email'),
            'password1': validated_data.get('password1'),
            'password2': validated_data.get('password2'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name')
        }
        request = self.client.build_request(method='POST',
                                            url=str(self.url.with_path('/registration/')),
                                            data=data
                                            )
        response = await self.send_request(request)
        if response.status_code == 201:
            return True
        else:
            return False

    async def login(self, validated_data):
        data = {
            'email': validated_data.get('email'),
            'password': validated_data.get('password')
        }
        request = self.client.build_request(method='POST',
                                            url=str(self.url.with_path('/login/')),
                                            data=data
                                            )
        response = await self.send_request(request)
        if response.status_code == 200:
            set_tokens(response.json(), self.user)
            return True
        else:
            return False

    async def profile(self):
        request = self.client.build_request(method='GET',
                                            url=str(self.url.with_path('/user-profile/get_profile/')),
                                            headers=self.get_header()
                                            )
        response = await self.send_request(request)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    async def profile_update(self, validated_data):
        data = {
            'email': validated_data.get('email'),
            'phone': validated_data.get('phone'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name')
        }
        request = self.client.build_request(method='PUT',
                                            url=str(self.url.with_path('/user-profile/update_profile/')),
                                            headers=self.get_header(),
                                            data=data)
        request.headers['Content-Type'] = 'multipart/form-data'
        response = await self.send_request(request)
        print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            return False

        # curl - X
        # 'PUT' \
        # 'http://137.184.201.122/user-profile/update_profile/' \
        # - H
        # 'accept: application/json' \
        # - H
        # 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0MDQ4MTgxLCJpYXQiOjE2NjQwNDgxMjEsImp0aSI6ImFiNjI3OWQ5NzU3YjRkNjdhMTJlYmM1YzExMWM5YTc2IiwidXNlcl9pZCI6MTF9.ewpd2Qjqd8LMy4nhk8jwsXlkb5QikhCzxNIIHaclxhg' \
        # - H
        # 'Content-Type: multipart/form-data' \
        # - H
        # 'X-CSRFTOKEN: HlNzABdqHEvDfj026i5BgKwHNYJWcjEJcZvIfKoYRM5f1XRwqcwnKgYOkJjsvqND' \
        # - F
        # 'first_name=Богдан' \
        # - F
        # 'last_name=Рожнятовский' \
        # - F
        # 'phone=+380939804334' \
        # - F
        # 'email=admin@admin.com' \
        # - F
        # 'profile_image='
