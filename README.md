# 2020-fall-bma-final
KAIST Business Modeling Analysis 기말 대체 과제 협업용 깃

# 협업 방식 ** 중요!! **
```
git clone https://github.com/kdchoi-mkt/2020-fall-bma-final.git
```
그 후에 작업을 하고싶다면,
```
git checkout -b <branch name>
```
를 통해서 새로 브랜치를 작성. 그 브랜치에서 작업을 완료하면,
```
git pull origin <branch name>
```
으로 진행

# 프로젝트 진행 방식
총 3가지 단계로 진행
1. 코드 전처리
2. 학습 및 모델링
3. 결과 보고

# 코드 전처리
코드 전처리는 두가지 데이터 셋을 통해서 이루어진다.
1. Clickstream dataset
    + 사람들이 몇 분동안, 어느 사이트에 방문했는지에 대한 기록
    + 자세한 사항은 ![click-stream 설명](click_stream/click_stream.md) 참조
2. Querystring dataset
    + 사람들이 어떤 검색을, 몇 번 했는지에 대한 기록
    + 자세한 사항은 ![query-string 설명](query_string/query_string.md) 참조

# 모델링
모델링은 Click-Stream dataset과 Query-String dataset 두개를 바탕으로 이루어진다.
+ 자세한 사항은 ![모델링 설명](modeling/modeling.md) 참조