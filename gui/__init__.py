# -*- coding: utf-8 -*-
from .helper import *

if get_dpi() < 120:
    dpi_cat = 'LowDPI'
else:
    dpi_cat = 'HighDPI'
