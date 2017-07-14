import sqlite3
import requests
import bs4
from datetime import datetime

# for log
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

conn = sqlite3.connect('main.db')
data = conn.execute("select * from gaoqing where download_url is null")
rows = data.fetchall()
for row in rows:
    url = row[2]
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,"html.parser")
    elems = soup.select('#post_content > p > span > a')
    if len(elems)==0:
        continue
    download_url = elems[-1]['href']
    gaoqing_id = row[0]
    sql = "UPDATE gaoqing set download_url = '%s' where ID='%s'"%(download_url,gaoqing_id)
    conn.execute(sql)
    print("complete 1 row")

conn.commit()

conn.close()
