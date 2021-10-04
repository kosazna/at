import re
from typing import Dict


class FilePattern(object):
    def __init__(self, pattern: str) -> None:
        self.pattern, self.kind = self._assert_pattern(pattern)
        self.nparts = 0
        self.variables = {}
        self._extract_vars(pattern)

    def __str__(self):
        return f"{self.kind}(parts={self.nparts}, variables={self.variables})"

    def _assert_pattern(self, pattern: str) -> str:
        langles = pattern.count("<")
        rangles = pattern.count(">")

        if langles != rangles:
            raise ValueError("Can't deduce parameters. Missing proper '<>'")

        if '_' in pattern and '@' in pattern:
            if '#' not in pattern:
                raise ValueError(
                    "Symbol '#' should be in pattern to indicate variable position relative to underscores")
            else:
                kind = "MixedPattern"  # "<shapefile#1>_<ota@8:12><tomeas@13:14>_<year#3>"
                return pattern, kind
        elif '_' in pattern:
            kind = "UnderscorePattern"  # "<shapefile>_<ota>"
            return pattern, kind
        elif '@' in pattern:
            kind = "PlaceholderPattern"  # "<ota@3:7><tomeas@8:9><enotita@10:11><gt@12:14>"
            return pattern, kind
        else:
            raise ValueError("At least one of '@' or '_' should be in pattern")

    def _extract_vars(self, pattern: str):
        regex = re.compile('<(.*?)>')
        parts = regex.findall(pattern)
        nparts = len(parts)
        self.nparts = nparts

        if self.kind == "MixedPattern":
            for part in parts:
                if '@' in part:
                    var_name, idxs = part.split('@')
                    start_idx, end_idx = idxs.split(':')

                    if start_idx:
                        _start = int(start_idx) - 1
                    else:
                        _start = 0

                    if end_idx:
                        _end = int(end_idx)
                    else:
                        _end = None

                    self.variables[var_name] = {'start': _start,
                                                'end': _end,
                                                'index': None}
                else:
                    var_name, idx = part.split('#')
                    self.variables[var_name] = {'start': None,
                                                'end': None,
                                                'index': int(idx)-1}
        elif self.kind == "UnderscorePattern":
            for idx, part in enumerate(parts):
                if '#' in part:
                    var_name, idx = part.split('#')
                    self.variables[var_name] = {'start': None,
                                                'end': None,
                                                'index': int(idx)-1}
                else:
                    self.variables[part] = {'start': None,
                                            'end': None,
                                            'index': idx}
        elif self.kind == "PlaceholderPattern":
            atcount = pattern.count('@')
            if atcount == nparts:
                for idx, part in enumerate(parts):
                    var_name, idxs = part.split('@')
                    start_idx, end_idx = idxs.split(':')

                    if start_idx:
                        _start = int(start_idx) - 1
                    else:
                        _start = 0

                    if end_idx:
                        _end = int(end_idx)
                    else:
                        _end = None

                    self.variables[var_name] = {'start': _start,
                                                'end': _end,
                                                'index': idx}
            else:
                raise ValueError(
                    f"Pattern contains {nparts} variables but {atcount} placeholders '@'")

    def match(self, text: str) -> Dict[str, str]:
        values = {}

        if self.kind == "MixedPattern":
            splitted = text.split('_')
            for var in self.variables:
                if self.variables[var]['index'] is not None:
                    values[var] = splitted[self.variables[var]['index']]
                else:
                    s = self.variables[var]['start']
                    e = self.variables[var]['end']
                    if e is None:
                        values[var] = text[s:]
                    else:
                        values[var] = text[s:e]
        elif self.kind == "UnderscorePattern":
            splitted = text.split('_')
            for var in self.variables:
                values[var] = splitted[self.variables[var]['index']]
        elif self.kind == "PlaceholderPattern":
            for var in self.variables:
                s = self.variables[var]['start']
                e = self.variables[var]['end']
                if e is None:
                    values[var] = text[s:]
                else:
                    values[var] = text[s:e]

        return values
