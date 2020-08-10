import pymysql
db = pymysql.connect(
    host='192.168.0.41', port=3306,
    user='scott', passwd='tiger',
    db='finalproject',
    charset='utf8', autocommit=True
    )
cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * from DB_leegippeum")
data = cursor.fetchall()
for infor in data:
    print("economic : %s " % infor['title'])
db.close()


#
# ❖ Create Table economic(release_date text, title text, link text);
# ❖ insert 2 record into economic
# ~$ pip install PyMySQL
# ~$ vi ./connect_mariadb.py
>>> import pymysql
>>> db = pymysql.connect(host='localhost', port=3306, user='root', passwd='tiger',
db='yojulabdb',charset='utf8',autocommit=True)
>>> cursor = db.cursor(pymysql.cursors.DictCursor)
>>> cursor.execute("SELECT * from economic")
>>> data = cursor.fetchall()
>>> for infor in data:
>>> print ("economic : %s " % infor['title'])
>>> db.close()

❖ 알아가기
➢ regexp로 검색
MariaDB [yojulabdb]> select * from economic where title regexp '[j]';
➢ Need Background Task Initialize
~$ sqlite3 db.sqlite3
sqlite> delete from background_task;



# Crawling and insert to DB(ex. ~$ sqlite3 ./db.sqlite3)
import requests; 
from bs4 
import BeautifulSoup; 
import sqlite3
>>> conn = sqlite3.connect('db.sqlite3')
>>> query = 'CREATE TABLE economic (title TEXT, link TEXT)'
>>> conn.execute(query)
>>> conn.commit(); conn.close()
>>> res = requests.get('http://media.daum.net/economic/')
>>> if res.status_code == 200:
>>> soup = BeautifulSoup(res.content, 'html.parser')
>>> links = soup.find_all('a', class_='link_txt')
>>> with sqlite3.connect("db.sqlite3") as con:
>>> cur = con.cursor()
>>> title = str(); link = str()
>>> for link in links:
>>> title = str.strip(link.get_text())
>>> link = link.get('href')
>>> cur.execute("INSERT INTO economic (title,link) VALUES (?,?)",(title,link))
>>> con.commit()
>>> print('task_crawling_daum : ', type(links), len(links))



#
pip install -U pip & pip install django-background-tasks
~$ python manage.py startapp crawling & python manage.py migrate
~$ vi ./crawling/crawling_tasks.py
from background_task import background; import time
@background
def task_hello(schedule=10, repeat=60):
time_tuple = time.localtime()
time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
print("task ... Hello World!", time_str)
~$ vi ./web_project/settings.py
INSTALLED_APPS = [
'background_task', # add
...,
]
~$ python manage.py migrate background_task
~$ vi ./web_project/urls.py
from crawling.crawling_tasks import task_hello # add
task_hello(schedule=60*1, repeat=60*2)
~$ python manage.py process_tasks
task ... Hello World! 06/16/2020, 03:40:54



#
sqlite3 db.sqlite3
sqlite> delete from background_task; # Task Initialize
~$ vi ./crawling/crawling_tasks.py
import requests; from bs4 import BeautifulSoup; import sqlite3
@background
def task_crawling_daum(schedule=2, repeat=60*3):



# add Crawling and insert to DB previously Code # add
time_tuple = time.localtime()
time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
print('task ... crawling_daum : ', time_str)
~$ vi ./web_project/urls.py
from crawling.crawling_tasks import task_crawling_daum # add
task_crawling_daum(schedule=60, repeat=60*2)
~$ python manage.py process_tasks
task_crawling_daum ... 325 06/16/2020, 03:40:55
...
~$ sqlite3 db.sqlite3
sqlite> select count(*) from background_task_completedtask;
