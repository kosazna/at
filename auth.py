# -*- coding: utf-8 -*-

import json
from typing import Callable, Tuple, Union

import requests

from at.io import write_json
from at.singleton import Singleton
from at.utils import user


class Authorize(metaclass=Singleton):
    TOKEN = '33e7a243e44dc089cd52476a3baebc59db6677e2'
    OWNER = 'kosazna'
    REPO = 'atauth'

    HEADERS = {'accept': 'application/vnd.github.v3.raw',
               'authorization': f"token {TOKEN}"}

    def __init__(self,
                 appname: str,
                 auth_filepath: Union[str, None] = None,
                 debug: bool = False):
        self.__url = f"https://api.github.com/repos/{self.OWNER}/{self.REPO}/contents/{appname}.json"
        self.auth_file = auth_filepath
        self.debug = debug
        self.user = user()
        self.actions = 0
        self._reload()

    def _reload(self) -> None:
        if not self.debug:
            self.r = requests.get(self.__url, headers=Authorize.HEADERS)
            self.user_access = json.loads(self.r.text)
            if self.auth_file is not None:
                write_json(filepath=self.auth_file, data=self.user_access)

    def user_is_licensed(self, domain: str) -> Tuple[bool, str]:
        if self.debug:
            return True, 'Debug Mode'

        if self.user_access:
            if domain not in self.user_access[self.user]:
                return False, f"{domain} is not in licensing info"
            else:
                try:
                    if self.actions < 10:
                        self.actions += 1
                        return self.user_access[self.user][domain], "User Authorised"
                    else:
                        self._reload()
                        self.actions += 1
                        return self.user_access[self.user][domain], "User Authorised"
                except KeyError:
                    return False, "User not authorised"
        else:
            return False, "Can't verify authentication due to internet access"


def licensed(appname: str, callback: Union[Callable, None] = print):
    def decorator(function):
        def wrapper(*args, **kwargs):
            auth = Authorize(appname=appname)
            authorised, info = auth.user_is_licensed(domain=function.__name__)
            if authorised:
                result = function(*args, **kwargs)
            else:
                callback(info)
                result = None
            return result
        return wrapper
    return decorator
