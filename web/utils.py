# -*- coding: utf-8 -*-

import random
import string
from os.path import join, splitext
from shutil import copyfileobj
from typing import Union

import requests
from fake_useragent import UserAgent

from at.logger import log

ua = UserAgent()


def get_headers(browser):
    if browser == 'Firefox':
        headers = {
            "User-Agent": f"{ua.firefox}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    else:
        headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": f"{ua.chrome}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }

    return headers


def get_user_agent(browser):
    return ua.firefox if browser == 'Firefox' else ua.chrome


def download_image(url: str,
                   destination: str,
                   save_name: Union[str, None] = None) -> None:
    if not url.startswith('https:'):
        url = f'https:{url}'
        
    r = requests.get(url, stream=True)
    url_file = url.split("/")[-1]
    ext = splitext(url_file)[1]

    if ext:
        _ext = ext
    else:
        _ext = '.jpg'

    if save_name is None:
        basename = ''.join(random.choices(string.ascii_letters + string.digits,
                                          k=32))
        filename = f"{basename}{_ext}"
    elif save_name == 'original':
        if ext:
            filename = url_file
        else:
            filename = f"{url_file}{_ext}"
    else:
        basename = save_name
        filename = f"{basename}{_ext}"

    dst = join(destination, filename)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(dst, 'wb') as f:
            copyfileobj(r.raw, f)
            log.success(f"Saved -> {filename}")
    else:
        log.error(f"Request failed -> {url}")
