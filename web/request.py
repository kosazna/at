# -*- coding: utf-8 -*-

from urllib.parse import urlencode

import httpx
import requests
from bs4 import BeautifulSoup

from at.web.utils import get_headers


def make_request(url: str):
    headers = get_headers("Firefox")

    r = requests.get(url, headers=headers)

    return r


def httpx_get(
    url: str,
    query_params: dict | None = None,
    headers: dict | None = None,
    basic_auth: str | None = None,
    bearer_token: str | None = None,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers["Authorization"] = f"Basic {basic_auth}"

    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    if query_params is not None:
        url = f"{url}?{urlencode(query_params)}"

    with httpx.Client(follow_redirects=True) as client:
        try:
            response = client.get(url=url, headers=headers, params=query_params)
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            return e.response
        except Exception as e:
            raise e


def httpx_post(
    url: str,
    data: dict,
    query_params: dict | None = None,
    headers: dict | None = None,
    basic_auth: str | None = None,
    bearer_token: str | None = None,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers["Authorization"] = f"Basic {basic_auth}"

    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    if query_params is not None:
        url = f"{url}?{urlencode(query_params)}"

    with httpx.Client(follow_redirects=True, timeout=30) as client:
        try:
            response = client.post(url=url, data=data, headers=headers, params=query_params)
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            return e.response
        except Exception as e:
            raise e


async def httpx_get_async(
    url: str,
    query_params: dict | None = None,
    headers: dict | None = None,
    basic_auth: str | None = None,
    bearer_token: str | None = None,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers["Authorization"] = f"Basic {basic_auth}"
    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        try:
            response = await client.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            return e.response
        except Exception as e:
            raise e


async def httpx_post_async(
    url: str,
    data: dict,
    query_params: dict | None = None,
    headers: dict | None = None,
    basic_auth: str | None = None,
    bearer_token: str | None = None,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers["Authorization"] = f"Basic {basic_auth}"
    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        try:
            response = await client.post(url, data=data, headers=headers, params=query_params)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            return e.response
        except Exception as e:
            raise e
        
async def httpx_client_get_async(
    client: httpx.AsyncClient,
    url: str,
    query_params: dict | None = None,
    headers: dict | None = None,
    basic_auth: str | None = None,
    bearer_token: str | None = None,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers["Authorization"] = f"Basic {basic_auth}"
    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    try:
        response = await client.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        return response
    except httpx.HTTPStatusError as e:
        return e.response
    except Exception as e:
        raise e


async def httpx_client_post_async(
    client: httpx.AsyncClient,
    url: str,
    data: dict | None = None,
    json: list | dict | None = None,
    query_params: dict | None = None,
    headers: dict | None = None,
    basic_auth: str | None = None,
    bearer_token: str | None = None,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if basic_auth is not None:
        headers["Authorization"] = f"Basic {basic_auth}"
    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    try:
        response = await client.post(url, data=data, json=json, headers=headers, params=query_params)
        response.raise_for_status()
        return response
    except httpx.HTTPStatusError as e:
        return e.response
    except Exception as e:
        raise e


def request_soup(url: str, lib: str = "requests", browser_headers: str = "Chrome"):
    if lib == "httpx":
        headers = get_headers(browser=browser_headers)
        r = httpx_get(url, headers=headers)
    else:
        r = make_request(url)

    soup = BeautifulSoup(r.text, "lxml")

    return soup
