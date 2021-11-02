# -*- coding: utf-8 -*-

from typing import List, Union

from at.web.element import Element
from bs4 import BeautifulSoup


def parse_soup(soup: BeautifulSoup,
               element: Element) -> Union[str, BeautifulSoup, None]:
    try:
        attrs = element.attrs

        if attrs:
            content = soup.find(element.TAG, element.attrs)
        else:
            content = soup.find(element.TAG)
    except KeyError:
        content = None

    if content is not None:
        if element.SUB is not None:
            return parse_soup(soup=content,
                              element=element.SUB)
        else:
            if element.ATTRIBUTE is not None:
                return content.get(element.ATTRIBUTE)
            return content.text if element.TEXT else content
    return None


def multi_parse_soup(soup: BeautifulSoup,
                     element: Element) -> Union[List[str],
                                                List[BeautifulSoup],
                                                list]:
    try:
        attrs = element.attrs

        if attrs:
            content = soup.find_all(element.TAG, element.attrs)
        else:
            content = soup.find_all(element.TAG)
    except KeyError:
        content = None

    if content is not None:
        elements = []
        if element.SUB is not None:
            for subcontent in content:
                elements.extend(multi_parse_soup(soup=subcontent,
                                                 element=element.SUB))
            return elements
        else:
            if element.ATTRIBUTE is not None:
                return [i.get(element.ATTRIBUTE) for i in content]
            return [i.text for i in content] if element.TEXT else content
    return list()
