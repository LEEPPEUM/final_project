from pymongo import MongoClient
client = MongoClient('mongodb://192.168.0.41:27017/')
ppeumdb = client.ppeumdb
land_sido = ppeumdb.land_sido.find()


print(land_sido)

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


query = "INSERT INTO LAND_SIDO_ppeum (stdrYear, stdrMt, ldCtprvnCode, ldCtprvnNm, ldCpsgCode, ldCpsgCodeNm, ldEmdLiCode, ldEmdLiCodeNm, pclndIndex, pclndChgRt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


for m in range(len(land_sido['byRegions']['field'])):
   land = land_sido['byRegions']['field']
   land[m]
   for n in range(len(land)):
      stdrYear = land[n].values[0]
      stdrMt = land[n].values[1]
      ldCtprvnCode = land[n].values[2]
      ldCtprvnNm = land[n].values[3]
      ldCpsgCode = land[n].values[4]
      ldCpsgCodeNm = land[n].values[5]
      ldEmdLiCode = land[n].values[6]
      ldEmdLiCodeNm = land[n].values[7]
      pclndInde = land[n].values[8]
      pclndChgRt = land[n].values[9]
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