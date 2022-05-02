# -*- coding: utf-8 -*-

from time import sleep
from typing import TypeVar

SeleniumWebDriver = TypeVar("SeleniumWebDriver")
SeleniumWebElement = TypeVar("SeleniumWebElement")


def one_time_scroll(driver: SeleniumWebDriver, scrollby: int = 1500):
    driver.execute_script(f"window.scrollTo(0, {scrollby});")


def scroll_down(driver: SeleniumWebDriver, scrollby: int = 1500, wait: float = 0.2):
    max_y = driver.execute_script("return document.body.scrollHeight")
    go_y = scrollby
    while go_y < max_y:
        driver.execute_script(f"window.scrollTo(0, {go_y});")
        go_y += scrollby
        sleep(wait)


def get_dom_element_attributes(driver: SeleniumWebDriver,
                               element: SeleniumWebElement) -> dict:
    script = """
    var items = {};
    for (index = 0; index < arguments[0].attributes.length; ++index) {
    items[arguments[0].attributes[index].name] =
        arguments[0].attributes[index].value;
    }
    var elemText = arguments[0].textContent.trim();

    if (elemText != "") {
    items.text = elemText;
    }

    return items;
    """

    _attrs = driver.execute_script(script, element)

    return _attrs
