from pymongo import MongoClient
client = MongoClient('mongodb://172.17.0.2:27017/')
mydb = client.mydb
board_info = mydb.board.find()
import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='tiger',db='yojulabdb',charset='utf8',autocommit=True)
cursor = conn.cursor()
query = "INSERT INTO economic (title,link) VALUES (%s,%s)"


for info in board_info: #mongodb 에 있는걸 옮겨라
   print(type(info), info['title'], info)
   title = info['title']
   link = str(info['likes'])
cursor.execute(query,(title,link))
conn.commit()
conn.close()