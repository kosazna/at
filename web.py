# -*- coding: utf-8 -*-

from typing import Union, List
from bs4 import BeautifulSoup


def parse(soup: BeautifulSoup,
          element_tag: str,
          element_class: str,
          text: bool = True) -> Union[str, BeautifulSoup, None]:
    try:
        content = soup.find(element_tag, {'class': element_class})
    except KeyError:
        content = None

    if content is not None:
        return content.text if text else content
    return None


def multi_parse(soup: BeautifulSoup,
                element_tag: str,
                element_class: str,
                text: bool = True) -> Union[List[str],
                                            List[BeautifulSoup],
                                            list]:
    try:
        content = soup.find_all(element_tag, {'class': element_class})
    except KeyError:
        content = None

    if content is not None:
        return [i.text for i in content] if text else content
    return list()
