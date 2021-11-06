# -*- coding: utf-8 -*-

from typing import List, Union

from at.web.element import Element
from bs4 import BeautifulSoup


def parse_soup(soup: BeautifulSoup,
               element: Element) -> Union[str, BeautifulSoup, None]:
    try:
        attrs = element.props

        if attrs:
            content = soup.find(element.tag, element.props)
        else:
            content = soup.find(element.tag)
    except KeyError:
        content = None

    if content is not None:
        if element.has_children():
            return parse_soup(soup=content,
                              element=element.child)
        else:
            if element.attribute is not None:
                return content.get(element.attribute)
            return content.text if element.return_text else content
    return None


def multi_parse_soup(soup: BeautifulSoup,
                     element: Element) -> Union[List[str],
                                                List[BeautifulSoup],
                                                list]:
    try:
        attrs = element.props

        if attrs:
            content = soup.find_all(element.tag, element.props)
        else:
            content = soup.find_all(element.tag)
    except KeyError:
        content = None

    if content is not None:
        elements = []
        if element.has_children():
            for subcontent in content:
                elements.extend(multi_parse_soup(soup=subcontent,
                                                 element=element.child))
            return elements
        else:
            if element.attribute is not None:
                return [i.get(element.attribute) for i in content]
            return [i.text for i in content] if element.return_text else content
    return list()
