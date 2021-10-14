from typing import List, Tuple, Union
import zipfile
from pathlib import Path

file_name = "D:/.temp/ktima.zip"
dst = "D:/.temp/copy_tests"
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
            elif filter_type == 'name':
                for fn, p in files.items():
                    if p.stem in file_filters:
                        f.extract(fn, dst)


unzip_file(file_name, dst, 'OIK', 'name')
