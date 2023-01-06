import time
import tqdm
import pandas as pd
import atexit

@atexit.register
def terminate():
    print('Finished')

# for x in tqdm.tqdm(range(0,20), "COPYING FILES", ncols=50, colour='blue', leave=True, bar_format="{l_bar}{bar}|"):  
#     b = "[" + "#" * x + ' ' * (100-x) + "]"
#     # print (b, end="/r")
#     time.sleep(0.1)
#     a = 10/0

df = pd.read_excel("D:/Terpos/LESJÖFORS-9999 - image.xlsx", dtype='string')
# df.to_json("D:/test.json", indent=2, orient="records", force_ascii=False)
df.to_pickle("D:/test.tar")
