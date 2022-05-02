# -*- coding: utf-8 -*-

from typing import List, Union

from at.web.element import Element
from bs4 import BeautifulSoup


def parse_soup(soup: BeautifulSoup,
               element: Element) -> Union[str, BeautifulSoup, None]:
    try:
        content = soup.find(**element.bs4_props())
    except KeyError:
        content = None

    if content is not None:
        if element.has_children():
            return parse_soup(soup=content,
                              element=element.child)
        else:
            if element.attribute is not None:
                if element.attribute == 'text':
                    return content.text
                return content.get(element.attribute)
            else:
                return content
    return None


def multi_parse_soup(soup: BeautifulSoup,
                     element: Element) -> Union[List[str],
                                                List[BeautifulSoup],
                                                list]:
    try:
        content = soup.find_all(**element.bs4_props())
    except KeyError:
        content = None

    if content is not None:
        elements = []
        if element.has_children():
            for subcontent in content:
                elements.extend(parse_soup(soup=subcontent,
                                           element=element.child))
            return elements
        else:
            if element.attribute is not None:
                if element.attribute == 'text':
                    return [i.text for i in content]
                return [i.get(element.attribute) for i in content]
            else:
                return content
    return None
