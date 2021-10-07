# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from pathlib import Path
import requests
import json

from at.date import timestamp
from at.io import write_json


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


class Authorize:
    TOKEN = '33e7a243e44dc089cd52476a3baebc59db6677e2'
    OWNER = 'kosazna'
    REPO = 'atauth'
    FILE = 'atktima.json'

    URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE}"

    HEADERS = {'accept': 'application/vnd.github.v3.raw',
               'authorization': f"token {TOKEN}"}

    def __init__(self, auth_filepath: str, debug: bool = False):
        self.debug = debug
        self.auth_file = auth_filepath
        self._reload()

    def _reload(self):
        self.r = requests.get(Authorize.URL, headers=Authorize.HEADERS)
        self.user_access = json.loads(self._r.text)
        self.actions = 0
        write_json(filepath=self.auth_file, data=self.user_access)

    def user_is_licensed(self, domain):
        if self.debug:
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
                print("Access to the service can't be verified. Contact support.")


print(check_auth_file("C:/Users/aznavouridis.k/AppData/Roaming/ktima/auth.json"))
