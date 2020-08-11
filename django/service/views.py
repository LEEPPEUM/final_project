from django.shortcuts import render
from django.shortcuts import HttpResponse
import pymysql
import pandas as pd
# Create your views here.
pddata=[]
pddatasets=[]

def pnucode_convert(front,back):
    
    front = front.astype(str).tolist()
    back = back.astype(str).tolist()
    c = front + back
    pnu_ten = "".join(c) # pnu 10자리로 저장
    return pnu_ten


def home(request):

    data = request.GET.copy()

    #get한 데이터 변수 저장
    si = data['si_gun_gu']
    dong = data['eup_myeon_dong']
    jiga = data['gongsijiga']

    #sql 연결요청 pdcode_table
    
    db = pymysql.connect(
    host='192.168.0.41', port=3306,
    user='scott', passwd='tiger',
    db='finalproject',
    charset='utf8', autocommit=True)

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * from pnucode_table")
    pddata= cursor.fetchall()

    #데이터프레임화 하여 조작
    pddata = pd.DataFrame(pddata)    
    a = pddata[pddata['name']==si].pnucode  #주소에 맞는 pnu code 추출 - 도시군구
    b = pddata[pddata['name']==dong].pnucode  #주소에 맞는 pnu code 추출 - 읍면동

    pnu_10 = pnucode_convert(a,b) # 함수 호출

    # sql 연결요청
    
    db = pymysql.connect(
    host='192.168.0.41', port=3306,
    user='scott', passwd='tiger',
    db='finalproject',
    charset='utf8', autocommit=True)

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * from datasets")
    datasets= cursor.fetchall()

    db.close()

    pdDatasets = pd.DataFrame(datasets)
    testdata = pdDatasets[pdDatasets['ldCode']==pnu_10]
    testdata = testdata.reset_index()
    #다시 dict type으로
    testdata_to_dict = testdata.to_dict('list')
    print(testdata_to_dict.keys())


    return render(request,'service/home.html',context=testdata_to_dict)
    # return render(request,'service/home.html',context=data)


def form(request):    
    return render(request,'service/form.html')
