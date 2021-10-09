# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Callable, Tuple, Union

import requests
from requests.exceptions import ConnectionError

from at.date import timestamp
from at.io import load_json, write_json, load_pickle, write_pickle
from at.singleton import Singleton
from at.utils import user, create_hex_string


def create_temp_auth(authdata: Union[str, Path],
                     appname: str,
                     licfolder: Union[str, Path, None],
                     date: Union[str, None] = None):
    if date is None:
        date_str = timestamp(time=False)
    else:
        date_str = date

    temp_auth = create_hex_string(f"{appname}-{date_str}")
    dst = Path(licfolder).joinpath(f"{temp_auth}.lic")

    if isinstance(authdata, dict):
        data = authdata
    else:
        auth_path = Path(authdata)
        if auth_path.suffix == '.json':
            data = load_json(auth_path)
        else:
            data = load_pickle(auth_path)

    write_pickle(dst, data)


def check_auth_file(filepath: Union[str, Path],
                    appname: str,
                    ref_hour: int = 12) -> Tuple[bool, dict]:
    authfile = Path(filepath)
    if authfile.exists():
        current_time = timestamp(return_object=True)
        creation_time = datetime.fromtimestamp(os.stat(filepath).st_ctime)

        auth = load_pickle(filepath)

        authfile.unlink()
        create_temp_auth(filepath, appname, authfile.parent)

        if timedelta(minutes=ref_hour) < current_time - creation_time:
            print("Credentials need to be refreshed soon")
            return False, auth
        else:
            return True, auth
    else:
        print("Authentication file does not exist")
        return False, dict()


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
                        create_temp_auth(authdata=self.auth,
                                         appname=self.appname,
                                         licfolder=self.auth_loc)
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

    def user_is_licensed(self, domain: str) -> Tuple[bool, str]:
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


if __name__ == "__main__":

    APPNAME = 'atcrawl'
    AUTHFOLDER = "C:/Users/aznavouridis.k/AppData/Roaming/.atcrawl"
    AUTHFILE = "C:/Users/aznavouridis.k/AppData/Roaming/.atcrawl/user.auth"

    # create_temporary_authentication(APPNAME, AUTHFOLDER)

    a = Authorize(appname=APPNAME,
                  auth_loc=AUTHFILE)

    @licensed('atcrawl')
    def find_images_run():
        print('ok')

    find_images_run()
