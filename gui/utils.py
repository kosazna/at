# -*- coding: utf-8 -*-
import sys
from dataclasses import dataclass
from typing import Optional, Tuple

from PyQt5.QtWidgets import QApplication, QWidget

HORIZONTAL = 'H'
VERTICAL = 'V'
PATH_PLACEHOLDER = "Paste path here or browse..."


def get_dpi():
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    app.quit()

    return int(dpi)


def set_size(widget: QWidget,
             size: Optional[Tuple[int]] = None,
             width: Optional[int] = None,
             height: Optional[int] = None):
    if size is not None:
        _width = size[0]
        _height = size[1]
        if _width is not None:
            widget.setFixedWidth(_width)
        if _height is not None:
            widget.setFixedHeight(_height)
    elif width is not None:
        widget.setFixedWidth(width)
    elif height is not None:
        widget.setFixedHeight(height)
    else:
        raise ValueError("At least one of size parameters must be provided")


@dataclass
class Color:
    name: str
    hex_value: str
    rgb_value: tuple

    def rgb(self, a=None):
        if a is None:
            return f"rgb{self.rgb_value!r}"
        else:
            _rgb = (*self.rgb_value, a)
            return f"rgba{_rgb!r}"

    def hex(self):
        return self.hex_value


@dataclass
class Gradient:
    value: str

    def rgb(self, a=None):
        return self.value


blue = Color('blue', '#0D6EFD', (13, 110, 253))
grey = Color('grey', '#6C757D', (108, 117, 125))
light_grey = Color('light_grey', '#D6D6D6', (221, 221, 221))
red = Color('red', '#EF3E4F', (239, 62, 79))
yellow = Color('yellow', '#FFC107', (255, 193, 7))
green = Color('green', '#2AD66B', (42, 214, 107))
teal = Color('teal', '#20C997', (32, 201, 151))
cyan = Color('cyan', '#0DCAF0', (13, 202, 79))
orange = Color('orange', '#FD7E14', (253, 126, 20))
dark = Color('dark', '#212529', (33, 37, 41))
white = Color('white', '#F8F8FF', (248, 248, 255))

blue_gradient = Gradient(
    "qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(13, 5, 81, 255), stop:1 rgba(36, 176, 189, 255))")


def make_stylesheet(background: Color = white,
                    foreground: Color = dark,
                    border=None,
                    radius: int = 3,
                    alpha: float = 0.8,) -> str:

    if border is None:
        _stylesheet = (f"background-color: {background.rgb(alpha)};\n"
                       f"color: {foreground.rgb()};\n"
                       f"border-radius: {radius}px;")
    else:
        _stylesheet = (f"background-color: {background.rgb(alpha)};\n"
                       f"border: 1px solid {border.rgb(1)};\n"
                       f"color: {foreground.rgb()};\n"
                       f"border-radius: {radius}px;")

    return _stylesheet


def make_color(background: Color, alpha: float = 0.8) -> str:
    return f"background-color: {background.rgb(alpha)};\n"
