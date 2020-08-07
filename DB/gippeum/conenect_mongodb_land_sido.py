from pymongo import MongoClient
import requests
import json

client = MongoClient('192.168.0.41:27017')
ppeumdb = client.ppeumdb

url = 'http://openapi.nsdi.go.kr/nsdi/FluctuationRateofLandPriceService/attr/getByRegion?reqLdCode=41&scopeDiv=B&format=json&numOfRows=1000000&pageNo=&authkey=b5b0b971327396765f3d8a'
# region only gyeonggi-do

for m in range(2015,2020):
    a = url + '&stdrYear=' + str(m)
    for n in range(1,13):
        b = a + '&stdrMt=' + str(n)
        res = requests.get(b)  
        if res.status_code == 200:
            data = json.loads(res.content)
            ppeumdb.land_sido.insert_one(data)
client.close()