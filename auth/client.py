# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Callable, Tuple, Union

import requests
from at.auth.utils import create_lic
from at.date import timestamp
from at.io import load_pickle
from at.singleton import Singleton
from at.text import create_hex_string
from at.utils import user
from requests.exceptions import ConnectionError


class Authorize(metaclass=Singleton):
    TOKEN = '33e7a243e44dc089cd52476a3baebc59db6677e2'
    OWNER = 'kosazna'
    REPO = 'atauth'

    HEADERS = {'accept': 'application/vnd.github.v3.raw',
               'authorization': f"token {TOKEN}"}

    def __init__(self,
                 appname: str,
                 auth_loc: Union[str, None] = None,
                 debug: bool = False):
        self.__url = f"https://api.github.com/repos/{self.OWNER}/{self.REPO}/contents/{appname}.json"
        self.appname = appname
        self.auth_loc = Path(auth_loc)
        self.debug = debug
        self.user = user()
        self.actions = 0
        self.auth = None
        self._reload()

    def _reload(self) -> None:
        if not self.debug:
            try:
                self.r = requests.get(self.__url, headers=Authorize.HEADERS)
                self.auth = json.loads(self.r.text)

                if self.auth_loc is not None:
                    if self.auth[self.user]['templic']:
                        create_lic(authdata=self.auth,
                                   appname=self.appname,
                                   folder=self.auth_loc)
            except ConnectionError:
                if self.auth_loc is not None:
                    date_str = timestamp(time=False)
                    temp_auth = create_hex_string(f"{self.appname}-{date_str}")
                    licfile = self.auth_loc.joinpath(f"{temp_auth}.lic")

                    if licfile.exists():
                        print("Temporary authentication in use")
                        content = load_pickle(licfile)
                        self.auth = content
                    else:
                        print("No temporary authentication found")
                        self.auth = {}
                else:
                    self.auth = {}

    def is_licensed(self, domain: str) -> Tuple[bool, str]:
        if self.debug:
            return True, 'Debug Mode'

        if self.auth:
            if domain not in self.auth[self.user]['action']:
                return False, f"{domain} is not in licensing info"
            else:
                try:
                    if self.actions < 10:
                        self.actions += 1
                        return self.auth[self.user]['action'][domain], "User Authorised"
                    else:
                        self._reload()
                        self.actions += 1
                        return self.auth[self.user]['action'][domain], "User Authorised"
                except KeyError:
                    return False, "User not authorised"
        else:
            return False, "Can't verify authentication due to internet access"


def licensed(appname: str,
             domain: Union[str, None] = None,
             callback: Union[Callable] = print):
    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            auth = Authorize(appname=appname)
            if domain is None:
                authorised, info = auth.is_licensed(domain=function.__name__)
            else:
                authorised, info = auth.is_licensed(domain=domain)
            if authorised:
                result = function(*args, **kwargs)
            else:
                callback(info)
                result = None
            return result
        return wrapper
    return decorator
