from abc import ABC, abstractmethod
from httpx import Response
from database.requests import set_tokens, get_refresh_token
from settings.config import HOST
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

    async def send_refresh_token(self):
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
                    response = await self.send_refresh_token()
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
        profile_image_path = None
        if 'profile_image' in validated_data and validated_data['profile_image'] is not None:
            image = validated_data['profile_image'].split('/')
            if image[1] != 'media':
                profile_image_path = validated_data.get('profile_image') or None
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


class AdsApiClient(BaseApiClient):

    def handler_response_errors(self, response: Response) -> Response:
        return response

    def get_header(self) -> dict:
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + get_token(self.user)
        }
        return headers

    async def create_ads(self, validated_data):
        image_path = validated_data.get('ads_image_src') or None
        data = {
            'address': validated_data.get('address'),
            'description': validated_data.get('description'),
            'area': validated_data.get('area'),
            'area_kitchen': validated_data.get('area_kitchen'),
            'price': int(validated_data.get('price')),
            'purpose': validated_data.get('purpose'),
            'rooms': validated_data.get('rooms'),
            'condition': validated_data.get('condition'),
            'residential_complex': validated_data.get('house')
        }
        request = self.client.build_request(method='POST',
                                            url=str(self.url.with_path('/ads/announcement/')),
                                            headers=self.get_header(),
                                            data=data,
                                            files={
                                                'images': open(image_path, 'rb')
                                            } if image_path is not None else {})

        response = await self.send_request(request)
        if response.status_code == 201:
            return response.json()
        else:
            return False

    async def get_ads(self, pk):
        request = self.client.build_request(method='GET',
                                            url=str(self.url.with_path(f'/ads/announcement-feed/{pk}/')),
                                            headers=self.get_header())

        response = await self.send_request(request)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    async def update_ads(self, validated_data, pk):
        data = {
            'address': validated_data.get('address'),
            'description': validated_data.get('description'),
            'area': validated_data.get('area'),
            'area_kitchen': validated_data.get('area_kitchen'),
            'price': validated_data.get('price'),
            'purpose': validated_data.get('purpose'),
            'rooms': validated_data.get('rooms'),
            'condition': validated_data.get('condition'),
            'balcony_or_loggia': validated_data.get('balcony_or_loggia'),
            'founding_document': validated_data.get('founding_document'),
            'layout': validated_data.get('layout'),
            'heating': validated_data.get('heating'),
            'payment_options': validated_data.get('payment_options'),
            'agent_commission': validated_data.get('agent_commission'),
            'communication': validated_data.get('communication')
        }
        request = self.client.build_request(method='PUT',
                                            url=str(self.url.with_path(f'/ads/announcement/{pk}/')),
                                            headers=self.get_header(),
                                            data=data)

        response = await self.send_request(request)
        print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            return False

    async def get_announcement_feed(self):
        request = self.client.build_request(method='GET',
                                            url=str(self.url.with_path('/ads/announcement-feed/')),
                                            headers=self.get_header())

        response = await self.send_request(request)
        if response.status_code == 200:
            return response.json()
        else:
            return False

