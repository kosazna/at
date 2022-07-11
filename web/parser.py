# -*- coding: utf-8 -*-

from typing import List, Union
from collections import ChainMap

from at.web.element import Element
from bs4 import BeautifulSoup
from bs4.element import Tag


def parse_soup(soup: BeautifulSoup,
               element: Element) -> Union[str, Tag, None]:
    try:
        if element.css_selector is not None:
            content = soup.select_one(element.css_selector)
        else:
            content = soup.find(**element.bs4_props())
    except KeyError:
        content = None

    if content is not None:
        if element.has_children():
            if isinstance(element.children, (list, tuple)):
                return dict(ChainMap(*[parse_soup(soup=content,
                                                  element=child)
                                       for child in element.children]))
            else:
                if element.children.many:
                    return multi_parse_soup(soup=content,
                                            element=element.children,
                                            orient='array')
                else:
                    return parse_soup(soup=content,
                                      element=element.children)
        else:
            if element.attribute is not None:
                if element.attribute == 'text':
                    _text = content.text
                    if _text:
                        return {element.name: _text}
                    return {element.name: element.default}
                else:
                    _attr = content.get(element.attribute)
                    if _attr:
                        return {element.name: _attr}
                    return {element.name: element.default}
            else:
                return content
    return {element.name: element.default}


def multi_parse_soup(soup: BeautifulSoup,
                     element: Element,
                     orient: str = 'dicts') -> Union[List[str],
                                                     List[Tag],
                                                     None]:
    try:
        if element.css_selector is not None:
            content = soup.select(element.css_selector)
        else:
            content = soup.find_all(**element.bs4_props())
    except KeyError:
        content = None

    if content is not None:
        elements = []
        if element.has_children():
            if isinstance(element.children, (list, tuple)):
                for subcontent in content:
                    elements.append(dict(ChainMap(*[parse_soup(soup=subcontent,
                                                               element=child)
                                                    for child in element.children])))
            else:
                for subcontent in content:
                    elements.append(parse_soup(soup=subcontent,
                                               element=element.children))
            return elements
        else:
            if element.attribute is not None:
                if element.attribute == 'text':
                    if orient == 'dicts':
                        return [{element.name: i.text} for i in content]
                    elif orient == 'array':
                        return {element.name: [i.text for i in content]}
                else:
                    if orient == 'dicts':
                        return [{element.name: i.get(element.attribute)} for i in content]
                    elif orient == 'array':
                        return {element.name: [i.get(element.attribute) for i in content]}     
            else:
                return content
    return None
