#
# 📈 **< 경기 지역의 토지부동산 투자가치평가 웹서비스 >**
Land  Real Estate Investment Valuation Web Service for the Gyeonggi area.
   
#

# **가설 설정 (Hypothesis)**

### **1. 독립변수**   
- 개별공시지가가 낮을수록
- 토지 면적이 넓을수록
- 개발제한구역과 자연환경보전지역을 제외한 나머지 개발이 가능한 용도지역
- 개발이 가능한 지목 종류(전, 답, 잡종지)
- 도로접면을 봤을때 도로와 가까울수록   
- 지형 높이가 경사 지지않고 완만할수록
- 지형 형상이 건물을 세우기에 좋을수록(건폐율, 용적률과 관련)
- 지가 지수가 낮을수록
- 지가 변동률이 낮을수록
- 주변 영업소의 교통량이 많을수록
- 주변 영업소 IC와의 거리가 짧을수록   
   
더 가치가 있고 개발에 용이한 매력적인 토지라고 가정한다.
   
### **2. 종속변수**   
- A급: 토지 그 자체로 매력적인 매물 
- B급: 개발이 필요하지만 괜찮은 매물
- C급: 투자가치가 없는 매물   
   
매물에 대한 평가를 하여 등급을 매기고자 한다.   
   
기존에 없던 종속변수이기 때문에 Machine Learning의 K-means 모델을 이용하여 새롭게 만들어 온전한 데이터셋을 만들 예정이다.   

#

# **서비스 아키텍처 (Service Architecture)**
   
- 클라이언트(Client)가 웹페이지에서 투자하고자 하는 지역과 개별공시지가 을 입력하면 그 시도구와 읍면동에 대해 머신러닝을 통해 만들어진 데이터셋 중에서 그 주소에 해당되는 매물을 서비스하고자 한다. 이때 개별공시지가는 클라이언트가 입력한 값으로 하여 매물의 평가 등급을 예측한다.
- 기존 데이터셋에 없는 클라이언트가 알고자하는 새로운 매물의 특성 정보(test_data) 입력 했을때 그에 대한 부동산 투자가치평가 서비스를 하고자 한다.
   
#
   
# **업무 분담 (The Division of Work)**
  
  
(ㄱㄴㄷ순)   
  
  
### **- 김소영(Kim Soyoung) :**
   [완료] 데이터 구조 기획 
   [완료] 경기도주소DB 업로드 1)pnu생성 2)db업로드   
   [완료] 토지특성정보 API DB업로드 -key:경기도pnu   
   [완료] 주소지 위경도 산출   
   [완료] 가장 가까운 고속도로 영업소 자동부여 코딩   
   [완료] 데이터 전처리 (with python)   
           1) one-hot encoding, outlier 처리,scaler   
           2) 전처리 단계별 Jamovi model power, vif check    
           3) 전처리 단계별 var check    
   [완료] 머신러닝 모델링(k-means)      
 
   
### **- 이기쁨(Lee Gippeum) :**   
   [완료] README.md 작성    
   [완료] 경기도 지가지수, 지가변동률 데이터   
   [완료] API 호출하여 MongoDB로 데이터 업로드   
   [완료] Convert MongoDB to MariaDB 작업   
   [완료] 개발용 git branch feature09로 작업하다가 master branch로 merge.   
   [완료] MariaDB 및 Python으로 MariaDB 연결하여 데이터 전처리   
   [완료] key를 이용하여 하나의 데이터셋으로 통합(inner join)   
   [완료] jamovi로 독립변수들간의 연관성을 살피고 이상치 확인, 범주형 변수의 특성 파악.   
   [진행중] 딥러닝 모델링       
   
   
### **- 이준오(Lee Juno) :**   
   [완료] 영업소별 교통량, IC/JCT 위치정보, 전국 영업소 위치정보 MariaDB에 업로드   
   [완료] 행정구역별 토지거래량 (경기도) 데이터 가공   
   [완료] mongoDB, MariaDB 서버 구축 & 관리   
   [진행중] Django 웹 서비스 구축 및 개발  
   [진행중] Python에서 Django와 MariaDB를 연결하여 웹 서비스 화면 제공.  
   [완료] Django README.md 작성
   
   
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
