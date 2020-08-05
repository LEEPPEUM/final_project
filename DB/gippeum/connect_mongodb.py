################

# from pymongo import MongoClient
# import requests
# import json
# # from bson.objectid import ObjectId

# client = MongoClient('mongodb://192.168.0.41:27017/')
# ppeumdb = client.ppeumdb
# url = 'http://openapi.nsdi.go.kr/nsdi/FluctuationRateofLandPriceService/attr/getByZoning?scopeDiv=B&format=json&numOfRows=1000000&authkey=51e9acfd7e4649c714d522&stdrYear='
# data = []
# for i in range(2015,2021):
#     res = requests.get(url+str(i))   
#     if res.status_code == 200:
#         url_json = json.loads(res.content)
#         data.append(url_json)
# ppeumdb.land.insert(data)
# client.close()

# # pymongo.errors.DocumentTooLarge: BSON document too large (59889718 bytes) - the connected server supports BSON document sizes up to 16777216 bytes.

# data['byZonings']['field']

################

# from pymongo import MongoClient
# import requests
# import json
# # from bson.objectid import ObjectId

# client = MongoClient('mongodb://192.168.0.41:27017/')
# ppeumdb = client.ppeumdb
# url = 'http://openapi.nsdi.go.kr/nsdi/FluctuationRateofLandPriceService/attr/getByZoning?scopeDiv=B&format=json&numOfRows=1000000&authkey=51e9acfd7e4649c714d522&stdrYear='
# for i in range(2015,2021):
#     res = requests.get(url+str(i))   
#     if res.status_code == 200:
#         data = json.loads(res.content)
#         ppeumdb.land.insert_many(data)
# client.close()

# # document must be an instance of dict, bson.son.SON, bson.raw_bson.RawBSONDocument, or a type that inherits from collections.MutableMapping


################
# from pymongo import MongoClient
# import requests
# import bsonjs
# from bson.raw_bson import RawBSONDocument

# client = MongoClient('192.168.0.41', 27017, document_class=RawBSONDocument)
# ppeumdb = client.ppeumdb
# url = 'http://openapi.nsdi.go.kr/nsdi/FluctuationRateofLandPriceService/attr/getByZoning?scopeDiv=B&format=json&numOfRows=1000000&authkey=51e9acfd7e4649c714d522&stdrYear='
# for i in range(2015,2021):
#     res = requests.get(url+str(i))   
#     if res.status_code == 200:
#         bson_data = bsonjs.loads(res.content)
#         raw_bson = RawBSONDocument(bson_data)
#         result = ppeumdb.land.insertMany(raw_bson)    # insert_one, insertOne, insert_many, insetMany
#         result.inserted_id  # ?
#         print(result.acknowledged)
# client.close()

# # BSON document too large (59889840 bytes) - the connected server supports BSON document sizes up to 16793598 bytes.


# GridFS
from pymongo import MongoClient
import requests
import bsonjs
from bson.raw_bson import RawBSONDocument
import gridfs

client = MongoClient('192.168.0.41', 27017, document_class=RawBSONDocument)
ppeumdb = client.ppeumdb
fs = gridfs.GridFS(ppeumdb)

url = 'http://openapi.nsdi.go.kr/nsdi/FluctuationRateofLandPriceService/attr/getByZoning?scopeDiv=B&format=json&numOfRows=1000000&authkey=51e9acfd7e4649c714d522&stdrYear='
for i in range(2015,2021):
    res = requests.get(url+str(i))   
    if res.status_code == 200:
        bson_data = bsonjs.loads(res.content)
        raw_bson = RawBSONDocument(bson_data)
        result = ppeumdb.land.insert_many(raw_bson)    # insert_one, insert_many
        result.inserted_ids  # ?
        print(result.acknowledged)
client.close()



# # find some record
# bson_record = ppeumdb.land.find_one({'test':'test01'}) #? ()

# # convert the record to json
# json_record = bsonjs.dumps(bson_record.raw)
# print(json_record)




# import pymongo
# import json 
# import datetime
# import bson.objectid

# def my_handler(x):
#     if isinstance(x, datetime.datetime):
#         return x.isoformat()
#     elif isinstance(x, bson.objectid.ObjectId):
#         return str(x)
#     else:
#         raise TypeError(x)

# db = pymongo.MongoClient().samples
# record = db.movies.find_one()
# # {u'_id': ObjectId('5692a15524de1e0ce2dfcfa3'), u'title': u'Toy Story 4',
# #   u'released': datetime.datetime(2010, 6, 18, 4, 0),}

# json_record = json.dumps(record, default=my_handler)
# # '{"_id": "5692a15524de1e0ce2dfcfa3", "title": "Toy Story 4", 
# #    "released": "2010-06-18T04:00:00"}'