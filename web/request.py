# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()


def get_headers(browser):
    if browser == 'firefox':
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
    return ua.firefox if browser == 'firefox' else ua.chrome


def request_soup(url, browser='firefox'):
    headers = get_headers(browser)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup
