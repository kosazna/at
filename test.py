from pathlib import Path
import re
from at.database import Query, SQLiteEngine, MySQLEngine, select

text = Path(
    "C:/Users/aznavouridis.k/.ktima/static/sql/select_ota_from_meleti.sql").read_text('utf-8')
text1 = Path(
    "C:/Users/aznavouridis.k/.ktima/static/sql/select_meletes.sql").read_text('utf-8')
data = Path("C:/Users/aznavouridis.k/.ktima/ktima.db")
# print(eval(re.search(r'{.*}', text).group()))
# print(re.sub(r'--{.*}', '', text).strip())


a = Query(text1).set(meleti="KT5-14").attrs(fetch='row')

b = Query("""SELECT name FROM atauth.app;""", fetch='rows')

dbs = SQLiteEngine(data)
mys = MySQLEngine("atauth")
print(mys.select(b))
# print(select(mys.connection.cursor(dictionary=True), b))

# print(dbs.select(a, dictionary=False))
# print(dbs.select(a))
# dbs.close_connection()
