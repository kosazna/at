# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay

from at.dataframe.io import excel2dataframes, export_dataframe
from at.dataframe.utils import df_date2str, df_str2date, iterrows
from at.date import DATE_MAPPER, timestamp
from at.deloitte.utils import read_SFFile
from at.io.object import FilterObject
from at.utils import parse_sheet_name


def load_config(filepath: str):
    filemap = excel2dataframes(filepath,
                               dtype='string',
                               sheets=['datafile_settings',
                                       'dates_info',
                                       'time_type_info'])

    _settings = filemap['datafile_settings'].fillna(
        '').set_index('property').to_dict()['value']
    _settings['date_format'] = DATE_MAPPER[_settings['date_format']]
    if _settings['data_contains_description_row'].lower() == 'yes':
        _settings['data_contains_description_row'] = True
    else:
        _settings['data_contains_description_row'] = False

    _dates = {
        'quantity_time_cols': filemap['dates_info']['quantity_time_column'].dropna().tolist(),
        'quantity_days_cols': filemap['dates_info']['quantity_days_column'].dropna().tolist(),
        'date_cols': filemap['dates_info']['date_columns'].dropna().tolist(),
        'public_holidays': pd.to_datetime(filemap['dates_info']['public_holidays'].dropna(),
                                          format=_settings['date_format']).tolist()
    }

    _types = filemap['time_type_info'].set_index(
        'time_type').to_dict(orient='index')

    return _settings, _dates, _types


def map_calendars(min_date: pd.Timestamp,
                  max_date: pd.Timestamp,
                  public_holidays: list[pd.Timestamp],
                  exclude_weekends: str,
                  exclude_public_holidays: str):
    all_days = pd.date_range(min_date, max_date).tolist()
    all_days_no_holidays = [
        d for d in all_days if d not in public_holidays]
    business_days = pd.date_range(min_date, max_date, freq='B').tolist()
    c_freq = CustomBusinessDay(holidays=public_holidays)
    business_days_no_holidays = pd.date_range(min_date,
                                              max_date,
                                              freq=c_freq).tolist()

    if exclude_weekends.lower() == 'no' and exclude_public_holidays.lower() == 'no':
        return all_days
    elif exclude_weekends.lower() == 'no' and exclude_public_holidays.lower() == 'yes':
        return all_days_no_holidays
    elif exclude_weekends.lower() == 'yes' and exclude_public_holidays.lower() == 'no':
        return business_days
    elif exclude_weekends.lower() == 'yes' and exclude_public_holidays.lower() == 'yes':
        return business_days_no_holidays
    else:
        return all_days


def process_file(data_filepath: Union[str, Path],
                 config: dict,
                 dates: dict,
                 times: dict):
    read_props = {
        'sheet_name': parse_sheet_name(config['sheet_name']),
        'skiprows': config['skiprows'] or None,
        'usecols': config['usecols'] or None
    }

    leaves, first = read_SFFile(data_filepath,
                                config['data_contains_description_row'],
                                **read_props)

    original_cols = leaves.columns

    leaves = df_str2date(leaves,
                         dates['date_cols'],
                         config['date_format'])

    start = dates['date_cols'][0]
    end = dates['date_cols'][1]

    leaves['range'] = leaves.apply(lambda df: pd.date_range(df[start],
                                                            df[end]),
                                   axis=1)

    min_date = leaves[start].min()
    max_date = leaves[end].max()

    leave_type_calendar = {}

    for lt, props in times.items():
        leave_type_calendar[lt] = map_calendars(min_date,
                                                max_date,
                                                dates['public_holidays'],
                                                **props)

    leaves_exploded = leaves.explode('range').reset_index(drop=True)

    idxs2del = []
    for idx, (time_type, date) in iterrows(leaves_exploded,
                                           [config['time_type_column'], 'range']):
        if time_type in leave_type_calendar:
            if date not in leave_type_calendar[time_type]:
                idxs2del.append(idx)

    leaves_cleaned = leaves_exploded.drop(idxs2del)

    leaves_cleaned[start] = leaves_cleaned['range']
    leaves_cleaned[end] = leaves_cleaned['range']

    for col in dates['quantity_days_cols']:
        if col in leaves_cleaned.columns:
            cond = leaves_cleaned[config['time_type_column']].isin(times.keys())
            leaves_cleaned.loc[cond, col] = '1'

    for col in dates['quantity_time_cols']:
        if col in leaves_cleaned.columns:
            cond = leaves_cleaned[config['time_type_column']].isin(times.keys())
            leaves_cleaned.loc[cond, col] = '8'

    leaves_cleaned = df_date2str(leaves_cleaned,
                                 dates['date_cols'],
                                 config['date_format'])

    leaves_cleaned = leaves_cleaned[original_cols]

    if first is not None:
        to_export = pd.concat([first, leaves_cleaned], ignore_index=True)
    else:
        to_export = leaves_cleaned

    tstamp = timestamp(filename_compatible=True)
    outfile = f"{tstamp}_{Path(data_filepath).stem}.xlsx"
    export_dataframe(outfile, to_export)


if __name__ == "__main__":
    config_file = "./LOA-configuration.xlsx"

    config, dates, times = load_config(config_file)

    fo = FilterObject.endswith(['.xls', '.xlsx'])

    for f in fo.search('./to_process'):
        try:
            process_file(f, config, dates, times)
        except Exception as e:
            print(f"File: {str(f)} - {e}")
