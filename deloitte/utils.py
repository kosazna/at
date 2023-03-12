# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Optional, Union
import pandas as pd
from at.dataframe.io import import_dataframe


def read_SFFile(filepath: Union[str, Path],
                description_row: bool = True,
                **kwargs) -> tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    _df = import_dataframe(filepath, **kwargs)

    if description_row:
        desc = _df.loc[[0]].copy()
        data = _df.drop(0, axis=0).copy()
    else:
        desc = None
        data = _df

    return data, desc
