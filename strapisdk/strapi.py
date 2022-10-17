from __future__ import annotations
from requests import Session
from strapisdk.config import (STRAPI_API_URL)


class Strapi:
    __url: str
    __prefix: str
    __token: str = None
    __session: Session = None
    __user = None

    def __init__(self, url: str = STRAPI_API_URL, prefix: str = "/api", token: str = None):
        self.__url = url
        self.__prefix = prefix
        self.__token = token
        self.__session = Session()

        if self.__token:
            self.setup_token()

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def api_url(self) -> str:
        return f'{self.url}{self.prefix}'

    @property
    def url(self) -> str:
        return self.__url

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def jwt(self) -> str:
        return self.__token

    @jwt.setter
    def jwt(self, value: str):
        self.__token = value
        self.setup_token()

    def setup_token(self):
        if self.jwt:
            self.session.headers.update({
                'Authorization': f'Bearer {self.jwt}'
            })
        else:
            self.session.headers.pop('Authorization', None)

    def build_api_route(self, path: str):
        return f'{self.api_url}/{path}'

    def login(self, identifier: str, password: str):
        with self.session.post(self.build_api_route('auth/local'), {
            'identifier': identifier,
            'password': password
        }) as handler:
            data = handler.json()

            if 'jwt' in data:
                self.__user = data.get("user", None)
                self.jwt = data.get("jwt")

            return data

    def parse_params(self, params: dict):
        parsed_params = {}
        for param_name, param_value in params.items():
            if isinstance(param_value, dict):
                for field_name, field_filter in params[param_name].items():
                    for filter_name, filter_value in field_filter.items():
                        key = f"{param_name}[{field_name}][{filter_name}]"
                        parsed_params[key] = filter_value
            else:
                parsed_params[param_name] = param_value

        return parsed_params

    def find(self, content_type: str, params=None):
        if params is None:
            params = {}
        params = self.parse_params(params)

        with self.session.get(self.build_api_route(f"{content_type}"), params=params) as handler:
            return handler.json()

    def find_one(self, content_type: str, id: int, params=None):
        if params is None:
            params = {}
        params = self.parse_params(params)

        with self.session.get(self.build_api_route(f"{content_type}/{id}"), params=params) as handler:
            return handler.json()

    def fetch_user(self):
        with self.session.get(self.build_api_route('users/me')) as handler:
            return handler.json()
