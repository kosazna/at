# -*- coding: utf-8 -*-
import re

def text2num(text:str):
    pattern = r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?'
    return re.findall(pattern, text)

print(text2num('1400,5'))