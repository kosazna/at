# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union
from at.singleton import Singleton
import requests
import json

from at.date import timestamp
from at.io import write_json
from at.utils import user


def check_auth_file(filepath: str, ref_hour: int = 12):
    if os.path.exists(filepath):
        current_time = timestamp(return_object=True)
        creation_time = datetime.fromtimestamp(os.stat(filepath).st_ctime)

        if timedelta(minutes=ref_hour) < current_time - creation_time:
            return False
        else:
            return True
    else:
        dirname = os.path.dirname(filepath)
        os.makedirs(dirname, exist_ok=True)
        write_json(filepath=filepath, data={})
        return False


class UnlicensedUserException(Exception):
    pass


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

    def _reload(self):
        if not self.debug:
            self.r = requests.get(self.__url, headers=Authorize.HEADERS)
            self.user_access = json.loads(self.r.text)
            if self.auth_file is not None:
                write_json(filepath=self.auth_file, data=self.user_access)

    def user_is_licensed(self, domain: str):
        if self.debug:
            return True

        if self.user_access:
            if domain not in self.user_access[self.user]:
                print(f"\n>>> {domain} is not licensed <<<\n")
                return True
            else:
                try:
                    if self.actions < 20:
                        self.actions += 1
                        return self.user_access[self.user][domain]
                    else:
                        self._reload()
                        self.actions += 1
                        return self.user_access[self.user][domain]
                except KeyError:
                    print("\n>>> User not authorised <<<\n")
                    return False
        else:
            print("\n>>> Can't verify authentication due to internet access <<<\n")
            return False


def licensed(appname: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            auth = Authorize(appname=appname)
            if auth.user_is_licensed(domain=function.__name__):
                result = function(*args, **kwargs)
            else:
                result = None
            return result
        return wrapper
    return decorator
