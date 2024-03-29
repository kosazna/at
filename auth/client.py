# -*- coding: utf-8 -*-

import json
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Callable, Optional, Tuple, Union
from dataclasses import dataclass
import requests
from at.auth.utils import create_lic
from at.date import timestamp
from at.io.utils import load_pickle
from at.logger import log
from at.singleton import Singleton
from at.text import create_hex_string
from at.utils import user
from requests.exceptions import ConnectionError
import os
from dotenv import load_dotenv

load_dotenv()

AUTHORISED = "Authorised"
UNAUTHORISED = "Unauthorised"


@dataclass
class AuthStatus:
    authorised: bool
    msg: str


class Authorize(metaclass=Singleton):
    TOKEN = os.getenv("GITHUB_TOKEN")
    OWNER = 'kosazna'
    REPO = 'atauth'

    def __init__(self,
                 appname: str,
                 auth_loc: Union[str, None] = None,
                 debug: bool = False,
                 token: Optional[str] = None):
        self.__url = f"https://raw.githubusercontent.com/{self.OWNER}/{self.REPO}/main/{appname}.json"
        self.appname = appname
        self.auth_loc = Path(auth_loc) if auth_loc is not None else auth_loc
        self.debug = debug
        self.user = user()
        self.actions = 0
        self.auth = None
        self.token = self.TOKEN if token is None else token
        self.headers = {'accept': 'application/vnd.github.v3.raw',
                        'authorization': f"token {self.token}"}
        self._reload()

    def set_alias(self, alias: str):
        self.user = alias
        log.success("Alias set successfully")

    def get_categories(self) -> list:
        if self.auth:
            if self.user in self.auth:
                return self.auth[self.user]['categories']
        return list()

    def _reload(self) -> None:
        if not self.debug:
            try:
                self.r = requests.get(self.__url, headers=self.headers)
                self.auth = json.loads(self.r.text)

                if self.auth_loc is not None:
                    try:
                        if self.auth[self.user]['templic']:
                            create_lic(authdata=self.auth,
                                       appname=self.appname,
                                       folder=self.auth_loc)
                    except KeyError:
                        log.info("Can't create temporary authentication")
            except JSONDecodeError:
                log.warning("Can't find GITHUB access token.")
                log.info("Reverting to temporary authentication...")
                if self.auth_loc is not None:
                    date_str = timestamp(time=False)
                    temp_auth = create_hex_string(f"{self.appname}-{date_str}")
                    licfile = self.auth_loc.joinpath(f"{temp_auth}.lic")

                    if licfile.exists():
                        log.warning("Temporary authentication in use")
                        content = load_pickle(licfile)
                        self.auth = content
                    else:
                        log.error("No temporary authentication found")
                        self.auth = {}
                else:
                    self.auth = {}
            except ConnectionError:
                if self.auth_loc is not None:
                    date_str = timestamp(time=False)
                    temp_auth = create_hex_string(f"{self.appname}-{date_str}")
                    licfile = self.auth_loc.joinpath(f"{temp_auth}.lic")

                    if licfile.exists():
                        log.warning("Temporary authentication in use")
                        content = load_pickle(licfile)
                        self.auth = content
                    else:
                        log.error("No temporary authentication found")
                        self.auth = {}
                else:
                    self.auth = {}

    def change_user_auth(self, status: bool):
        if self.debug:
            return
            
        if self.user in self.auth:
            for domain in self.auth[self.user]['action']:
                self.auth[self.user]['action'][domain] = status

    def is_licensed(self,
                    domain: Optional[str] = None,
                    category: Optional[str] = None) -> Tuple[bool, str]:
        if self.debug:
            return True, 'Debug Mode'

        if self.auth:
            try:
                if category is not None and domain is not None:
                    if category not in self.auth[self.user]['categories']:
                        return False, UNAUTHORISED
                    if domain not in self.auth[self.user]['action']:
                        return False, f"License deactivated for action"
                    else:
                        if self.actions < 10:
                            self.actions += 1
                            _valid = self.auth[self.user]['action'][domain]
                            _info = AUTHORISED if _valid else UNAUTHORISED
                            return _valid, _info
                        else:
                            self._reload()
                            self.actions += 1
                            _valid = self.auth[self.user]['action'][domain]
                            _info = AUTHORISED if _valid else UNAUTHORISED
                            return _valid, _info
                elif category is not None and domain is None:
                    if category in self.auth[self.user]['categories']:
                        if self.actions < 10:
                            self.actions += 1
                            return True, AUTHORISED
                        else:
                            self._reload()
                            self.actions += 1
                            return True, AUTHORISED
                    return False, UNAUTHORISED
                else:
                    if domain not in self.auth[self.user]['action']:
                        return False, f"'{domain}' is not in licensing info"
                    else:
                        if self.actions < 10:
                            self.actions += 1
                            _valid = self.auth[self.user]['action'][domain]
                            _info = AUTHORISED if _valid else UNAUTHORISED
                            return _valid, _info
                        else:
                            self._reload()
                            self.actions += 1
                            _valid = self.auth[self.user]['action'][domain]
                            _info = AUTHORISED if _valid else UNAUTHORISED
                            return _valid, _info
            except KeyError:
                return False, "User not authorised"
        else:
            return False, "Can't verify authentication due to internet access"


def licensed(appname: str,
             domain: Optional[str] = None,
             category: Optional[str] = None,
             callback: Callable = log.error):
    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            auth = Authorize(appname=appname)
            if domain is None:
                fname = function.__name__
                authorised, info = auth.is_licensed(domain=fname,
                                                    category=category)
            else:
                authorised, info = auth.is_licensed(domain=domain,
                                                    category=category)
            if authorised:
                result = function(*args, **kwargs)
            else:
                callback(info)
                result = AuthStatus(authorised, info)
            return result
        return wrapper
    return decorator
