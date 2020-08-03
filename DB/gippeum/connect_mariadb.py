import pymysql
db = pymysql.connect(host='localhost',port=3306,user='root',passwd='tiger',db='yojulabdb',charset='utf8',autocommit=True)

cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT* from economic")
data = cursor.fetchall()
for infor in data:
    print("economic : %s " % infor['title'])
db.close()