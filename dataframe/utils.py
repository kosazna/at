# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Iterable, List, Optional, Union

import pandas as pd

from at.logger import log


def export_dataframe(filepath: Union[str, Path], data: pd.DataFrame, **kwargs):
    suffix = Path(filepath).suffix
    str_filepath = str(filepath)
    allowed = ('.xlsx', '.csv', '.xml', '.json')
    allowed_str = ', '.join(allowed)

    if suffix not in allowed:
        raise ValueError(f"{suffix} not supported. Try one of {allowed_str}.")

    if suffix == '.xlsx':
        data.to_excel(str_filepath, index=False, **kwargs)
        return True
    elif suffix == '.csv':
        data.to_csv(str_filepath, index=False, **kwargs)
        return True
    elif suffix == '.xml':
        data.to_xml(str_filepath, index=False, **kwargs)
        return True
    elif suffix == '.json':
        data.to_json(str_filepath, orient='records', force_ascii=False,
                     indent=2, **kwargs)
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


def df_str2date(df: pd.DataFrame,
                columns: Iterable[str],
                date_format: Optional[str]):
    _df = df.copy()

    for date_col in columns:
        _df[date_col] = pd.to_datetime(_df[date_col], format=date_format)

    return _df


def df_date2str(df: pd.DataFrame, columns: Iterable[str], date_format: str):
    _df = df.copy()

    for date_col in columns:
        _df[date_col] = _df[date_col].dt.strftime(date_format=date_format)

    return _df
