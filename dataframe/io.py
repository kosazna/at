# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Union

import pandas as pd


def dataframes2excel(filepath: Union[str, Path],
                     data: Union[List[pd.DataFrame], Dict[str, pd.DataFrame]],
                     mode: str = 'w'):

    with pd.ExcelWriter(filepath, mode=mode, engine='openpyxl') as writer:
        if isinstance(data, (list, tuple)):
            for idx, df in enumerate(data, 1):
                df.to_excel(writer, index=False, sheet_name=f"Sheet{idx}")
        elif isinstance(data, dict):
            for sheet_name, df in data.items():
                df.to_excel(writer, index=False, sheet_name=sheet_name)


def excel2dataframes(filepath: Union[str, Path]) -> Dict[str, pd.DataFrame]:
    data_map = {}

    with pd.ExcelFile(filepath, engine='openpyxl') as excelfile:
        for sheet_name in excelfile.sheet_names:
            data_map[sheet_name] = excelfile.parse(sheet_name)

    return data_map


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
