from pymongo import MongoClient
client = MongoClient('mongodb://192.168.0.41:27017/')
ppeumdb = client.ppeumdb
land_sido = ppeumdb.land_sido.find() # _id.count() = 60, each year and month, 2015 ~ 2019


import pymysql
conn = pymysql.connect(
   host='192.168.0.41', 
   port=3306, 
   user='scott', 
   passwd='tiger',
   db='finalproject',
   charset='utf8', autocommit=True
   )

cursor = conn.cursor()


query = "INSERT INTO finalproject.LAND_SIDO_ppeum (stdrYear, stdrMt, ldCtprvnCode, ldCtprvnNm, ldCpsgCode, ldCpsgCodeNm, ldEmdLiCode, ldEmdLiCodeNm, pclndIndex, pclndChgRt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


for sido in land_sido: # _id Of land_sido: 60, _id Of sido : 1
   field = sido['byRegions']['field']    # {'byRegions':{'field':[{},{},...,{}]},{numOfRows:10000},{pageNo:1}}
   # values = field[0].values()
   # print(values)
   # values = list(values)
   # print(values[2])
   # for value in values:
   #    print(value)
   for n in range(len(field)):   # field: Gyeonggi-do, JAU, 2015
      values = field[n].values()
      values = list(values)
      #  
      stdrYear = values[2]
      stdrMt = values[3]
      ldCtprvnCode = values[5]
      ldCtprvnNm = values[6]
      ldCpsgCode = values[0]
      ldCpsgCodeNm = values[7]
      ldEmdLiCode = values[1]
      ldEmdLiCodeNm = values[8]
      pclndIndex = values[9]
      pclndChgRt = values[10]
      #
      cursor.execute(query,(stdrYear, stdrMt, ldCtprvnCode, ldCtprvnNm, ldCpsgCode, ldCpsgCodeNm, ldEmdLiCode, ldEmdLiCodeNm, pclndIndex, pclndChgRt))
conn.commit()
conn.close()




# import pymysql
# db = pymysql.connect(
#     host='192.168.0.41', port=3306,
#     user='scott', passwd='tiger',
#     db='finalproject',
#     charset='utf8', autocommit=True
#     )
# cursor = db.cursor(pymysql.cursors.DictCursor)
# cursor.execute("SELECT * from LAND_SIDO_ppeum")
# data = cursor.fetchall()
# for infor in data:
#    #  print("LAND_SIDO : %s " % infor['title'])
# db.close()