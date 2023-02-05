# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, Union

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
                date_format: Optional[str] = None) -> pd.DataFrame:
    _df = df.copy()

    for date_col in columns:
        if date_col in _df.columns:
            _df[date_col] = pd.to_datetime(_df[date_col], format=date_format)

    return _df


def df_date2str(df: pd.DataFrame,
                columns: Iterable[str],
                date_format: str) -> pd.DataFrame:
    _df = df.copy()

    for date_col in columns:
        if date_col in _df.columns:
            _df[date_col] = _df[date_col].dt.strftime(date_format=date_format)

    return _df


def iterrows(df: pd.DataFrame,
             cols: Optional[Union[str, Iterable[str]]] = None) -> Tuple[pd.Index, Any]:
    if isinstance(cols, str):
        if cols not in df.columns:
            raise KeyError(f"[{cols}] not in dataframe columns")
    else:
        if cols is not None:
            missing_cols = []
            for col in cols:
                if col not in df.columns:
                    missing_cols.append(col)
            if missing_cols:
                msg = '-'.join(missing_cols)
                raise KeyError(f"[{msg}] not in dataframe columns")

    single_col = False

    if cols is not None:
        if isinstance(cols, str):
            single_col = True
        else:
            _cols = [df[col] for col in cols]
    else:
        _cols = [df[col] for col in df.columns]

    if single_col:
        for idx, val in zip(df.index, df[cols]):
            yield idx, val
    else:
        for idx, *vals in zip(df.index, *_cols):
            yield idx, vals
