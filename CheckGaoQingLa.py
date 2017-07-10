# check the http://gaoqing.la/ have new episode

import requests
import bs4
import sqlite3

# check the website
res = requests.get('http://gaoqing.la/')
soup = bs4.BeautifulSoup(res.text,"html.parser")
elems = soup.select('#post_container > li > div > div.thumbnail > a')
list = []
for elem in elems:
    item = {}
    item['title'] = elem['title']
    item['url'] = elem['href']
    item['img_url'] = elem.contents[1]['src']
    list.append(item)
print("Geted the page")

# print(list)

#  save to the database
# Title Url Imgurl downloadurl date
conn = sqlite3.connect('main.db')
cursor = conn.cursor()
conn.execute('''CREATE TABLE if not exists GAOQING 
       (ID        integer PRIMARY KEY autoincrement,
       TITLE           CHAR(400),
       URL            CHAR(400) UNIQUE,
       IMG_URL      CHAR(400),
       DOWNLOAD_URL   CHAR(400),
       CREATEDTIME    TimeStamp NOT NULL DEFAULT (datetime('now','localtime')));''')

rownumber = 0

for item in list:
    keys = str(item.keys())[9:].replace('[', '').replace(']', '')
    vals = str(item.values())[11:].replace('[', '').replace(']', '')
    cursor.execute('INSERT or IGNORE INTO gaoqing %s VALUES %s' % (keys, vals))
    rownumber += cursor.rowcount

conn.commit()
conn.close()

print("%s rows has inserted"%rownumber)

#data = conn.execute("select * from gaoqing")
#rows =data.fetchall()
#print(rows)
