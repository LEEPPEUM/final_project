# **< 경기도 지역 순수토지에 대한 부동산 투자가치평가 서비스 >**     
#


# **업무 분담**   
(ㄱㄴㄷ순)   

**- 소영 :**   
   [완료] 경기도주소DB 업로드 1)pnu생성 2)db업로드   
   [완료] 토지특성정보 API DB업로드 -key:경기도pnu   
   [완료] 주소지 위경도 산출   
   [완료] 가장 가까운 고속도로 영업소 자동부여 코드   
   [완료] 딥러닝용 데이터프레임 구축 1)아웃라이어, 표준화 2)kmeans 적용   
   [진행중] 머신러닝 모델링(k-means), Python으로 데이터 전처리      
 
   
**- 기쁨 :**   
   [완료] 경기도 지가지수, 지가변동률 데이터   
   [완료] API 호출하여 MongoDB로 데이터 업로드   
   [완료] Convert MongoDB to MariaDB 작업   
   [완료] 개발용 git branch feature09로 작업하다가 master branch로 merge.   
   [완료] MariaDB 및 Python으로 MariaDB 연결하여 데이터 전처리   
   [완료] key를 이용하여 하나의 데이터셋으로 통합(inner join)   
   [진행중] 딥러닝 모델링   
   [진행중] one-hot convert 방식      
   

**- 준오 :**   
   [완료] 영업소별 교통량, IC/JCT 위치정보, 전국 영업소 위치정보 MariaDB에 업로드   
   [완료] 행정구역별 토지거래량 (경기도) 데이터 가공   
   [완료] mongoDB, MariaDB 서버 구축 & 관리   
   [진행중] Django 웹 서비스 구축 및 개발       
#



# PROJECT_SCHEDULE   


### 1. 주제, 가설 세우기 (_7/29_)       
- 서비스 대상: 부동산업자, 개인 부동산 투자자**
- 개별공시지가, 실거래가, 지가변동률, 교통량, 도로와의 거리, 토지 특성 정보를 이용하여 투자가치가 있을 토지를 예측하여 소비자에게 서비스하고자 한다. 머신러닝을 이용하여 Clutering을 해보거나 개별공시지가를 종속변수로 하여 실거래가와 비교하고 고평가(거품가격), 적정가격, 저평가(미래투자가치)를 구분하고자 한다.

   

### 2. 데이터 수집, 독립변수, 종속변수 정하기 (_7/30_)
- 공공 데이터 포털, 한국도로공사 고속도로 공공 데이터 포털, 국토교통부 국가공간정보포털에서 Open API 방식으로 데이터를 가져올 계획이다. Daily Crawling으로 데이터를 MongoDB에 우선 담고 MariaDB로 변환하려고 한다.   
- 종속변수로 개별공시지가, 표준공시지가, 실거래가를 고려하고 있다.    
   

### 3. 데이터 전처리 (_8/1_)
- 토지 부동산은 도로와의 거리가 중요하므로 토지 주소와 고속도로 IC 주소를 Python의 haversign을 이용하여 거리계산을 하고 새로운 독립변수로 삼고자 한다.
- Open API로 불러온 정보 중 필요한 부분만 추출한다.   
   

### 4. DB 구축 (_8/3_)
- 각 토지의 주소에 맞게 RDB의 JOIN 기능을 사용하여 각각에 맞는 개별공시지가, 지가변동률, 교통량 등을 맞추려고 한다.
- 전국 도로명주소 DB 활용   
   

### 5. ML/DL (_8/6_)
- Traditional MachinLearning 중 Clustering 방식으로 종속변수가 없다는 가정 하에 진행하여 군집이 어떻게 이루어지는지 살펴본다.
- 종속변수를 개별공시지가, 실거래가의 차로 해본다.
- 개별공시지가를 종속변수로 우선 삼고 실거래가를 참고하여 고평가, 적정가격, 저평가를 구분한다.   
   

### 6. Django (_8/9_)
- Python의 Web Service Framework인 Django로 소비자에게 토지 부동산 투자 서비스를 웹에서 제공하고자 한다. 소비자가 원하는 주소지를 선택하면 그 토지에 대한 예상 가격이 나온다. 
- 저평가된 토지라면 현 시세와 비교하여 투자 가치가 있을지 판단이 가능하다.   
   

### 7. PPT, 보고서 작성 (_8/12_)
- 가설과 분석방법, 분석결과 등 자세히 기술한다.   
   

### 8. 최종 발표 (_8/14_)
