# -*- coding: utf-8 -*-
from typing import List, Tuple, Union
import zipfile
from pathlib import Path

file_name = "D:/.temp/KT2-11_ΠΑΡΑΔΟΤΕΑ_ΨΗΦΙΑΚΗ ΒΑΣΗ ΧΩΡΙΚΩΝ ΣΤΟΙΧΕΙΩΝ.zip"
dst = "D:/.temp/unzip"
SHP_EXTS = ('.shp', '.shx', '.dbf')

# with zipfile.ZipFile(file_name, 'r') as zipf:
#     all_files = {f: Path(f) for f in zipf.namelist()}

#     for f, p in all_files.items():
#         if p.suffix in SHP_EXTS:
#             print(p.is_file())


def unzip_file(src: Union[str, Path],
               dst: Union[str, Path],
               filters: Union[str, List[str], Tuple[str], None] = None,
               filter_type: str = 'name'):

    if filters is not None:
        if isinstance(filters, str):
            file_filters = [filters]
        else:
            file_filters = filters

    with zipfile.ZipFile(src, 'r') as f:
        if filters is None:
            f.extractall(dst)
        else:
            files = {filename: Path(filename) for filename in f.namelist()}
            if filter_type == 'suffix':
                for fn, p in files.items():
                    if p.suffix in file_filters:
                        f.extract(fn, dst)
            elif filter_type == 'filename':
                for fn, p in files.items():
                    if p.stem in file_filters:
                        f.extract(fn, dst)
            elif filter_type == 'dir':
                for fn, p in files.items():
                    for filter_item in file_filters:
                        if filter_item in p.parts:
                            f.extract(fn, dst)


otas = [
    "22003",
    "22006",
    "22008",
    "22011",
    "22012",
    "22019",
    "22022",
    "22033",
    "22044",
    "22049",
    "22050",
    "22055",
    "22057",
    "22058",
    "22059",
    "22062",
    "22063",
    "22066",
    "22070",
    "22071",
    "22076",
    "22085",
    "22093",
    "22095",
    "22098",
    "22100",
    "22101",
    "22103",
    "22104",
    "22105",
    "22106",
    "22107",
    "22110",
    "22116",
    "22123",
    "22125",
    "22126",
    "22129",
    "22132",
    "22134",
    "22140",
    "22141"
]

unzip_file(file_name, dst, otas, 'filename')
