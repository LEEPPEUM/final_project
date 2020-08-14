# 🤠 DJango로 구현한 웹서비스 화면 구성

## + _구현되어 있는 기능_ 
#### form.html 화면에서 값을 요청받을 때 마다 동작한다.

1. form.html에서 입력받을 form을 제공, 사용자가 form에 맞게 데이터를 입력

---
![form1](https://user-images.githubusercontent.com/45375353/90223691-8004d280-de49-11ea-952b-99c364da6865.JPG)


---

2. service.views.py에 있는 home 함수에서 form에서 보내준 값을 가져와 데이터를 저장한다.
---
```python
data = request.GET.copy()

#get한 데이터 변수 저장
si = data['si_gun_gu']
dong = data['eup_myeon_dong']
jiga = data['gongsijiga']
```
---

3. 주소 - (시군구), (읍면동) 한글로 들어온 데이터를 pnu코드(숫자)로 변환하기 위하여 mariaDB의 pnucode_table과 매칭하여 변환
---
```python
#db 가져오기
cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * from pnucode_table")
pddata= cursor.fetchall()

#데이터프레임화하여 조작
pddata = pd.DataFrame(pddata)    
a = pddata[pddata['name']==si].pnucode  #주소에 맞는 pnu code 추출 - 도시군구
b = pddata[pddata['name']==dong].pnucode  #주소에 맞는 pnu code 추출 - 읍면동

pnu_10 = pnucode_convert(a,b) # 함수 호출
```
---
---

```python
# pnucod를 10자리로 만드는 함수 (시군구) + (읍면동)
def pnucode_convert(front,back):    
    front = front.astype(str).tolist()
    back = back.astype(str).tolist()
    c = front + back
    pnu_ten = "".join(c) # pnu 10자리로 저장
    return pnu_ten

```
---

4. 만들어진 pnucode(10자리로) DB에 있는 dataset과 매칭 시킨다. DB를 전체 가져오고 python으로 조작 후 One-hot encoding으로 범주형 변수들을 미리 바꿔준다. 그리고 사용자가 입력한 공시지가로 전부 변경시킨다.
```python
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
testdata = pdDatasets[pdDatasets['ldCode']==pnu_10]
testdata = testdata.reset_index()


#ont-hot encoding
testdata = pd.get_dummies(pdDatasets,columns=['prposArea1','lndcgrCode','tpgrphHgCode','tpgrphFrmCode','roadSideCode'])
testdata = testdata[testdata['ldCode']==pnu_10]    
testdata = testdata.reset_index()


try :
    testdata['pblntfPclnd'] = test[test['pblntfPclnd']] = jiga # 입력받은 공시지가로 모든 컬럼 변경
except :
    print('ignore')
```
---
5. 아래에서 로드하여 가져올 딥러닝 모델에 새롭게 만든 데이터셋을 넣어주기 위해 똑같은 형태와 타입으로 맞춰주는 작업을 한다. 
```python
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
```
---
6. 로드하여 가져온 모델로 종속변수를 뽑아내여 등급으로 바꿔주는 작업

```python
 ### 모델로드 & predict
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
```

---
7. home.html에 위에서 조작한 데이터를 보내주어 서비스화면에 표시해야 하기 때문에 dict타입으로 변경해주는 작업과 service에서 보여줄 독립변수만 보내주기위해 zip(리스트형태로 된 데이터들을 dict타입으로 묶어주기 위해 사용: [list1],[list2],[list3]...) 으로 묶는다.

- testdata_to_dict도 dictionary 타입인데 zip으로 한 번더 dictionary type으로 묶어주는 이유 : return 하여 html로 보낼 때 반복문하나로 여러개의 요소를 가져올 수 있게 하기 위해 사용한다. 

```python
#다시 dict type으로   
testdata_to_dict = testdata.to_dict('list')  
mylist = zip(testdata_to_dict['juso'],testdata_to_dict['pblntfPclnd'],testdata_to_dict['pnu']) 
context_ = {
    'mylist':mylist,
}  
```
--> **_결과화면은 값이 잘 전달되는지 보기위해 구현한 것임.(구현하고자 하는 서비스와 다를 수 있음)_**
```html
<table id ="resultTable">
    <tr>
        <th>주소</th>
        <th>지가</th>
        <th>등급</th>
    </tr>                       
    {% for v1,v2,v3 in mylist %} 
    <tr>
        <td>{{v1}}</td>                
        <td>{{v2}}</td>
        <td>{{v3}}</td>
    </tr>
    {% endfor %}   
</table>
```
--> **_결과화면_**

---
![KakaoTalk_20200814_153329193](https://user-images.githubusercontent.com/45375353/90224597-dcb4bd00-de4a-11ea-8dee-36efaa8d631e.png)

---
![KakaoTalk_20200814_153357264](https://user-images.githubusercontent.com/45375353/90224600-dd4d5380-de4a-11ea-89d6-e0f70400f4b1.png)
---

