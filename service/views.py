from django.shortcuts import render
from django.shortcuts import HttpResponse
import pymysql
import pandas as pd
import numpy as np
import tensorflow as tf
import sklearn
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import load_model

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
    host='127.0.0.1', port=3306,
    user='scott', passwd='tiger',
    db='finalproject',
    charset='utf8', autocommit=True)

    #db 가져오기
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
    host='127.0.0.1', port=3306,
    user='scott', passwd='tiger',
    db='finalproject',
    charset='utf8', autocommit=True)

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * from datasets")
    datasets= cursor.fetchall()

    db.close()

    pdDatasets = pd.DataFrame(datasets)
    
   
    
    #ont-hot encoding
    testdata = pd.get_dummies(pdDatasets,columns=['prposArea1','lndcgrCode','tpgrphHgCode','tpgrphFrmCode','roadSideCode'])
    testdata = testdata[testdata['ldCode']==pnu_10]    
    testdata = testdata.reset_index()
    

    try :
        testdata['pblntfPclnd'] = testdata[testdata['pblntfPclnd']] = jiga # 입력받은 공시지가로 모든 컬럼 변경
    except :
        print('ignore')
        
    #print('지가대치',testdata)
    
      

    ### predict form에 맞게 데이터 변환

    testdata= testdata[['pnu', 'ldCode', 'pblntfPclnd', 'lndpclAr', 'pclndIndex', 'pclndChgRt', 'juso', 'trafficAmount', 'distance', 'prposArea1_11', 'prposArea1_13', 'prposArea1_14', 'prposArea1_15', 'prposArea1_16', 'prposArea1_21', 'prposArea1_22', 'prposArea1_23', 'prposArea1_32', 'prposArea1_33', 'prposArea1_41', 'prposArea1_42', 'prposArea1_43', 'prposArea1_44', 'prposArea1_62', 'prposArea1_63', 'prposArea1_64', 'prposArea1_71', 'prposArea1_81', 'lndcgrCode_01', 'lndcgrCode_02', 'lndcgrCode_03', 'lndcgrCode_04', 'lndcgrCode_05', 'lndcgrCode_08', 'lndcgrCode_09', 'lndcgrCode_10', 'lndcgrCode_11', 'lndcgrCode_12', 'lndcgrCode_13', 'lndcgrCode_14', 'lndcgrCode_15', 'lndcgrCode_16', 'lndcgrCode_17', 'lndcgrCode_18', 'lndcgrCode_19', 'lndcgrCode_20', 'lndcgrCode_21', 'lndcgrCode_22', 'lndcgrCode_23', 'lndcgrCode_24', 'lndcgrCode_25', 'lndcgrCode_27', 'lndcgrCode_28', 'tpgrphHgCode_00', 'tpgrphHgCode_01', 'tpgrphHgCode_02', 'tpgrphHgCode_03', 'tpgrphHgCode_04', 'tpgrphHgCode_05', 'tpgrphFrmCode_00', 'tpgrphFrmCode_01', 'tpgrphFrmCode_02', 'tpgrphFrmCode_03', 'tpgrphFrmCode_04', 'tpgrphFrmCode_05', 'tpgrphFrmCode_06', 'tpgrphFrmCode_07', 'tpgrphFrmCode_08', 'roadSideCode_00', 'roadSideCode_01', 'roadSideCode_02', 'roadSideCode_03', 'roadSideCode_04', 'roadSideCode_05', 'roadSideCode_06', 'roadSideCode_07', 'roadSideCode_08', 'roadSideCode_09', 'roadSideCode_10', 'roadSideCode_11', 'roadSideCode_12']]
    
    nct = testdata[['lndpclAr','pblntfPclnd','pclndIndex','pclndChgRt','trafficAmount','distance']]
    ct = testdata.drop(['lndpclAr','pblntfPclnd','pclndIndex','pclndChgRt','trafficAmount','distance','pnu','juso','ldCode',],axis=1)
    
    
    # #scaling
 
    scaler = MinMaxScaler()    
    for i in nct:
        nct[i]=scaler.fit_transform(nct[i].values.reshape(-1,1))
    

    # 넘파이 변환

    ctnp = ct.to_numpy()
    nctnp = nct.to_numpy()
    
    
    pred_dataset = np.concatenate((nctnp,ctnp),axis=1)
      
    print(nctnp)
   
    ### 모델로드 & predict
    from keras.models import load_model    

    new_model = load_model('model_DL.h5')
    
    result_y = []
    result_y =new_model.predict_classes([pred_dataset])
    grade=[]
    
    for i in result_y:
        if result_y[i]==0 :
            grade+='A'
        elif result_y[i]==1 :
            grade+='B'
        elif result_y[i]==2 :
            grade+='C' 
        elif result_y[i]==3 :
            grade+='D'
            

    #다시 dict type으로   
    testdata_to_dict = testdata.to_dict('list')  
    mylist = zip(testdata_to_dict['juso'],testdata_to_dict['pblntfPclnd'],grade) 
    context_ = {
        'mylist':mylist,
    }  

    return render(request,'service/home.html',context=context_)   


def form(request):    
    return render(request,'service/form.html')
