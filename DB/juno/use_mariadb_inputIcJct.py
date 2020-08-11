import pymysql
import requests
import json
import pandas as pd
#db
db = pymysql.connect(host='localhost',port=3306,user='root',passwd='tiger',db='finalproject',charset='utf8',autocommit=True)

cursor = db.cursor(pymysql.cursors.DictCursor)


# data 가져오기 
# url = 'http://data.ex.co.kr/openapi/locationinfo/locationinfoIc?type=json'
# header = {'key': '3561488592'}
# response = requests.get(url,header)
# response.status_code # 200 이면 정상
# icJct_dict = json.loads(response.content) # json으로 load
# ic_jct = pd.DataFrame(icJct_dict['list'])

# print(ic_jct)
# for i in range(len(ic_jct)):
#     routName = ic_jct.routeName[i]
#     routeNo = ic_jct.routeNo[i]
#     icCode = ic_jct.icCode[i]
#     icName = ic_jct.icName[i]
#     xValue = ic_jct.xValue[i]
#     yValue = ic_jct.yValue[i]
#     cursor.execute("INSERT INTO IC_JCT_LOC_juno (routName,routeNo,icCode,icName,xValue,yValue) VALUES (%s,%s,%s,%s,%s,%s)",(routName,routeNo,icCode,icName,xValue,yValue))

# Pnu code

code = pd.read_csv("/home/sundooedu/문서/final_project/DB/juno/법정동코드정리.csv",encoding = 'cp949')
print(code)

for i in range(len(code)):
    name = code.name[i]
    pnucode = code.pnucode[i]
    cursor.execute("INSERT INTO pnucode_table(name,pnucode) VALUES (%s,%s)",(name,str(pnucode)))

data = cursor.fetchall()


#for infor in data:
#    print("economic : %s " % infor['title'])

db.close()