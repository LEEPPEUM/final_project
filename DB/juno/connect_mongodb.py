from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://172.17.0.2:27017/')
fp = client.finalproject
data = {'title':'mongoDB 보기', 'tags' : ['디비서비스']}
board_info = fp.board.insert_one(data)

data = [{"name": "Ram","age":"26", "city" : "Hyderabad"}, { "name":"Rahim","age":"27","city":"Bangalore"}]

res = fp.board.insert_many(data)
print("Data inserted ......", res.inserted_ids)
board_info = fp.board.find()
for info in board_info:
    print(info)
client.close()

#mydb.board.update({'_id':ObjectId('5f..7')},{'$push':{'tags':'MySQL'}})



