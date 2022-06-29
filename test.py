from pathlib import Path
import re
from at.database import Query, SQLiteEngine, MySQLEngine, select
from at.number import decimal2float, str2num, text2num
from at.io.utils import load_json
from dataclasses import make_dataclass, astuple
from at.data.item import Item, item_factory
from at.data.collection import ItemCollection

text = Path(
    "C:/Users/aznavouridis.k/.ktima/static/sql/select_ota_from_meleti.sql")
text1 = Path(
    "C:/Users/aznavouridis.k/.ktima/static/sql/select_meletes.sql")
skroutz = "C:/Users/aznavouridis.k/Desktop/skroutz.sql"
data = Path("C:/Users/aznavouridis.k/Desktop/terpos.db")

datas = [{'link': '/s/30475704/Sony-Xperia-1-III-5G-Single-SIM-12GB-256GB-Frosted-Black.html?from=featured&product_id=85046151',
  'image': None,
  'price': '999,00 €',
  'specs': 'Μοντέλο: 2021,  Οθόνη: OLED 6.5", Μπαταρία: 4500mAh',
  'title': 'Sony Xperia 1 III 5G Single SIM (12GB/256GB) Frosted Black'},
 {'link': '/s/30662995/Samsung-Galaxy-A52s-5G-Dual-SIM-6GB-128GB-Awesome-Black.html',
  'image': '//c.scdn.gr/images/sku_main_images/030662/30662995/large_20210830101603_samsung_galaxy_a52s_128gb_awesome_black.jpeg',
  'price': 'από271,88 €',
  'specs': 'Μοντέλο: 2021,  Οθόνη: Super AMOLED 6.5", Μπαταρία: 4500mAh',
  'title': 'Samsung Galaxy A52s 5G Dual SIM (6GB/128GB) Awesome Black'}]

json_config = load_json("D:/.temp/.dev/.aztool/atparser/skroutz.config.json")
SkroutzItem = item_factory("SkroutzItem", json_config['config']['fields'])
# items = map(lambda x: SkroutzItem(**x).astuple(), datas)
items = ItemCollection.from_dicts(SkroutzItem, datas)
a = Query.from_file(skroutz).set(datastream=items.get_data('tuple'))

# b = Query("""SELECT c.customerName, SUM(p.amount) as `Total`
# FROM classicmodels.payments as p
# RIGHT JOIN classicmodels.customers as c ON c.customerNumber=p.customerNumber
# GROUP BY c.customerNumber;""", fetch='rows')

dbs = SQLiteEngine(data)
# dbs.insert(a)

num = "από1,16€"
print(text2num(num))
# mys = MySQLEngine("classicmodels")
# print(mys.select(b, False))


# result = mys.select(b, False)
# for i in result:
#     print(decimal2float(i[1]))
# print(select(mys.connection.cursor(dictionary=True), b))

# print(dbs.select(a, dictionary=False))
# print(dbs.select(a))
# dbs.close_connection()
