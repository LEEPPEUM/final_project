# 🤠 DJango로 구현한 웹서비스 화면 구성

## + _구현되어 있는 기능_ 
#### form.html 화면에서 값을 요청받을 때 마다 동작한다.

1. form.html에서 입력받을 form을 제공, 사용자가 form에 맞게 데이터를 입력

---
![form](https://user-images.githubusercontent.com/45375353/90083379-451d7480-dd4d-11ea-926e-0530662abbc1.JPG)

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

4. 만들어진 pnucode(10자리로) DB에 있는 dataset과 매칭 시킨다. DB를 전체 가져오고 python으로 조작 후
공시지가를 사용자가 입력한 값으로 모두 바꿔준다.
```python
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

try :
    testdata['pblntfPclnd'] = test[test['pblntfPclnd']] = jiga # 입력받은 공시지가로 모든 컬럼 변경
except :
    print('ignore')
```
---
5. home.html에 위에서 조작한 데이터를 보내주어 서비스화면에 표시해야 하기 때문에 dict타입으로 변경해주는 작업과 service에서 보여줄 독립변수만 보내주기위해 zip(리스트형태로 된 데이터들을 dict타입으로 묶어주기 위해 사용: [list1],[list2],[list3]...) 으로 묶는다.

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
        <th>pnu</th>
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
--> **_결과화면 예시_**

---
![result](https://user-images.githubusercontent.com/45375353/90083365-3df66680-dd4d-11ea-9e7a-22940cb953eb.JPG)

---

## _+ 구현해야 하는 기능_
- 위의 5번 동작을 하기 전에 딥러닝으로 생성된 모델에 pnucode로 매칭된 데이터와 입력받은 데이터로 predict 한다. 
- predict하고 나온 결과 값 (범주형)을 각각 매칭된 주소에 맞게 home.html에 나올 수 있게 구현해야한다.
