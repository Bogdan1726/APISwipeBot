from abc import ABC, abstractmethod
from httpx import Response
from database.requests import set_tokens, get_refresh_token
from settings.config import HOST
from aiogram.client.session import aiohttp
from yarl import URL
from database.requests import get_token, update_token, logout
import httpx
from requests_toolbelt import MultipartEncoder


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
                    response_data = response.json()
                    if 'access' in response_data:
                        request.headers['Authorization'] = 'Bearer ' + response_data['access']
                        response = await client.send(request)
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
        profile_image_path = validated_data.get('profile_image_src') or None
        data = {
            'email': validated_data.get('email'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'phone': validated_data.get('phone'),
        }
        request = self.client.build_request(method='PUT',
                                            url=str(self.url.with_path('/user-profile/update_profile/')),
                                            headers=self.get_header(),
                                            data=data,
                                            files={
                                                'profile_image': open(profile_image_path, 'rb')
                                            } if profile_image_path is not None else {})

        response = await self.send_request(request)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    async def user_ads(self):
        request = self.client.build_request(method='GET',
                                            url=str(self.url.with_path('/ads/announcement-feed/get_my_announcement/')),
                                            headers=self.get_header())
        response = await self.send_request(request)
        if response.status_code == 200:
            return response.json()
        else:
            return False
