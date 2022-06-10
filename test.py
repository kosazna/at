from pathlib import Path
import re
from at.database.object import QueryObject
from at.database.sqlite import SQLiteEngine
text = Path("C:/Users/aznavouridis.k/.ktima/static/sql/select_ota_from_meleti.sql").read_text('utf-8')
data = Path("C:/Users/aznavouridis.k/.ktima/ktima.db")
# print(eval(re.search(r'{.*}', text).group()))
# print(re.sub(r'--{.*}', '', text).strip())

a = QueryObject(text).set(meleti="KT5-14")
dbs = SQLiteEngine(data)
print(a)