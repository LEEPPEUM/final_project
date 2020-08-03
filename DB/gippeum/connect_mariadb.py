import pymysql
db = pymysql.connect(host='192.168.0.41',port=3306,user='scott',passwd='tiger',db='finalproject',charset='utf8',autocommit=True)

cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * from DB_leegippeum")
data = cursor.fetchall()
for infor in data:
    print("economic : %s " % infor['title'])
db.close()