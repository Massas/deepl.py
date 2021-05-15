from abc import ABCMeta, abstractmethod
import json
from typing import Union

import aiohttp
import requests

from .errors import (
    BadRequest,
    Forbidden,
    HTTPException,
    NotFound,
    PayloadTooLarge,
    URITooLong,
    TooManyRequests,
    QuotaExceeded,
    ServiceUnavailable,
    InternalServerError
)


class Adapter(metaclass=ABCMeta):
    def __init__(self, authentication_key: str, *, pro=False):
        self.base_url_free = 'https://api-free.deepl.com/'
        self.base_url_pro = 'https://api.deepl.com/'
        self.api_version = 'v2'
        self.auth_key = authentication_key
        self.pro = pro

    @abstractmethod
    def request(self, method, path, payload={}, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_translated_text(self, payload):
        raise NotImplementedError()

    @abstractmethod
    def get_usage(self):
        raise NotImplementedError()

    @abstractmethod
    def get_supported_languages(self):
        raise NotImplementedError()

    def _check_status(self, status_code, response, data) -> Union[dict, list]:
        if 200 <= status_code < 300:
            return data
        message = data.get('message', '') if data else ''
        if status_code == 400:
            raise BadRequest(response, message)
        elif status_code == 403:
            raise Forbidden(response, message)
        elif status_code == 404:
            raise NotFound(response, message)
        elif status_code == 413:
            raise PayloadTooLarge(response, message)
        elif status_code == 414:
            raise URITooLong(response, message)
        elif status_code == 429:
            raise TooManyRequests(response, message)
        elif status_code == 456:
            raise QuotaExceeded(response, message)
        elif status_code == 503:
            raise ServiceUnavailable(response, message)
        elif 500 <= status_code < 600:
            raise InternalServerError(response, message)
        else:
            raise HTTPException(response, message)


class RequestsAdapter(Adapter):
    def request(self, method, path, payload={}, **kwargs):
        headers = {'content-type': 'x-www-form-urlencoded'}
        payload['auth_key'] = self.auth_key

        url = self.base_url_pro if self.pro else self.base_url_free
        url += self.api_version + path

        resp = requests.request(method, url, params=payload, headers=headers)
        try:
            data = resp.json()
        except json.JSONDecodeError:
            data = None
        return self._check_status(resp.status_code, resp, data)
        

    def get_translated_text(self, payload):
        data = self.request('POST', '/translate', payload)
        return data['translations'][0]['text']

    def get_usage(self):
        data = self.request('POST', '/usage')
        return data

    def get_supported_languages(self):
        data = self.request('POST', '/languages')
        return data


class AiohttpAdapter(Adapter):

    async def request(self, method, path, payload={}, **kwargs):
        headers = {'content-type': 'x-www-form-urlencoded'}
        payload['auth_key'] = self.auth_key

        url = self.base_url_pro if self.pro else self.base_url_free
        url += self.api_version + path

        async with aiohttp.request(
                method, url, params=payload, headers=headers) as resp:
            try:
                data = await resp.json(content_type=None)
            except json.JSONDecodeError:
                data = None
            status_code = resp.status
        return self._check_status(status_code, resp, data)

    async def get_translated_text(self, payload):
        data = await self.request('POST', '/translate', payload)
        return data['translations'][0]['text']

    async def get_usage(self):
        data = await self.request('POST', '/usage')
        return data

    async def get_supported_languages(self):
        data = await self.request('POST', '/languages')
        return data
