from pathlib import Path
import re
from at.database.object import Query
from at.database.sqlite import SQLiteEngine

text = Path(
    "C:/Users/aznavouridis.k/.ktima/static/sql/select_ota_from_meleti.sql").read_text('utf-8')
text1 = Path(
    "C:/Users/aznavouridis.k/.ktima/static/sql/select_meletes.sql").read_text('utf-8')
data = Path("C:/Users/aznavouridis.k/.ktima/ktima.db")
# print(eval(re.search(r'{.*}', text).group()))
# print(re.sub(r'--{.*}', '', text).strip())



a = Query(text1).set(meleti="KT5-14")
dbs = SQLiteEngine(data)

print([dict(r) for r in dbs.select(a)])
dbs.close_connection()
