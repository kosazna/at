# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Iterable, List, Optional, Union

import pandas as pd

from at.logger import log


def export_dataframe(filepath: Union[str, Path], data: pd.DataFrame):
    suffix = Path(filepath).suffix
    str_filepath = str(filepath)
    allowed = ('.xlsx', '.csv', '.xml', '.json')
    allowed_str = ', '.join(allowed)

    if suffix not in allowed:
        raise ValueError(f"{suffix} not supported. Try one of {allowed_str}.")

    if suffix == '.xlsx':
        data.to_excel(str_filepath, index=False)
        return True
    elif suffix == '.csv':
        data.to_csv(str_filepath, index=False)
        return True
    elif suffix == '.xml':
        data.to_xml(str_filepath, index=False)
        return True
    elif suffix == '.json':
        data.to_json(str_filepath, orient='records', force_ascii=False)
        return True
    else:
        return False


def make_raw_dataframe(data: Union[List[dict], List[tuple], pd.DataFrame],
                       columns: Optional[Iterable] = None):
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, list):
        try:
            first_element = data[0]
        except KeyError:
            log.error('Empty dataset')
            return None

        if isinstance(first_element, dict):
            return pd.DataFrame(data, dtype='string')
        elif isinstance(first_element, tuple):
            if columns is None:
                log.error(
                    'When dataset is a list of tuples, columns must be provided')
                return None
            return pd.DataFrame(data, columns=columns, dtype='string')