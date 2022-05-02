# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from at.web.utils import get_headers


def make_request(url: str):
    headers = get_headers('Firefox')

    r = requests.get(url, headers=headers)

    return r


def request_soup(url: str):
    r = make_request(url)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup
