# -*- coding: utf-8 -*-

import pandas as pd
from typing import List, Union

from at.data.collection import ItemCollection


def collection2dataframe(collection: ItemCollection,
                         columns: Union[List[str], None] = None) -> pd.DataFrame:
    df = pd.DataFrame(collection.items)

    if collection.types is not None:
        df = df.astype(dtype=collection.types)

    if columns is not None:
        df.columns = columns

    return df
