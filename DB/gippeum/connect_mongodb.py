from pymongo import MongoClient
import requests
import json
# from bson.objectid import ObjectId
client = MongoClient('mongodb:/192.168.0.41:27017/')
ppeumdb = client.ppeumdb
url = 'http://openapi.nsdi.go.kr/nsdi/FluctuationRateofLandPriceService/attr/getByZoning?scopeDiv=B&format=json&numOfRows=1000000&authkey=51e9acfd7e4649c714d522&stdrYear='
data = []
for i in range(2015,2021):
    res = requests.get(url+str(i))   
    if res.status_code == 200:
        url_json = json.loads(res.content)
        data.append(url_json)
ppeumdb.land.insert(data)
client.close()