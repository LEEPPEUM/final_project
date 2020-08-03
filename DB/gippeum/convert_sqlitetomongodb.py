import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('db.sqlite3') # db connect
query='SELECT * FROM economic'


c = conn.cursor()
c.execute(query)
data = c.fetchall()


# connect mongodb
from pymongo import MongoClient
client = MongoClient('mongodb://172.17.0.2:27017/')
mydb = client.mydb


econ_data =[]
for i in range(len(data)): # mongodb에 넣기위에 키,밸류 값으로 세팅
  econ_data+=[{"date" : data[i][0], "title": data[i][1], "link": data[i][2]}]


res = mydb.economic.insert_many(econ_data)
print("Data inserted .....",res.inserted_ids)
economic_info = mydb.economic.find()
for info in economic_info:
  print(info)


print(mydb.economic.find({'date':'20200702'}))