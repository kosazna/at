# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import httpx
from urllib.parse import urlencode

from at.web.utils import get_headers


def make_request(url: str):
    headers = get_headers('Firefox')

    r = requests.get(url, headers=headers)

    return r


def httpx_get(url: str, query_params: dict = None, headers: dict = None, basic_auth: str = None, bearer_token: str = None):
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers['Authorization'] = f'Basic {basic_auth}'

    if bearer_token is not None:
        headers['Authorization'] = f'Bearer {bearer_token}'

    if query_params is not None:
        url = f"{url}?{urlencode(query_params)}"

    with httpx.Client() as client:
        try:
            response = client.get(
                url=url,
                headers=headers,
                follow_redirects=True
            )
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            return e.response if hasattr(e, 'response') else e
        except Exception as e:
            raise e
        
def httpx_post(url: str, data: dict, query_params: dict = None, headers: dict = None, basic_auth: str = None, bearer_token: str = None):
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers['Authorization'] = f'Basic {basic_auth}'

    if bearer_token is not None:
        headers['Authorization'] = f'Bearer {bearer_token}'

    if query_params is not None:
        url = f"{url}?{urlencode(query_params)}"

    with httpx.Client() as client:
        try:
            response = client.post(
                url=url,
                data=data,
                headers=headers,
                timeout=30,
                follow_redirects=True
            )
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            return e.response if hasattr(e, 'response') else e
        except Exception as e:
            raise e


def request_soup(url: str, lib: str = "requests", browser_headers: str = "Chrome"):
    if lib == "httpx":
        headers = get_headers(browser=browser_headers)
        r = httpx_get(url, headers=headers)
    else:
        r = make_request(url)

    soup = BeautifulSoup(r.text, 'lxml')

    return soup
