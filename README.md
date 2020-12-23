# 2020-fall-bma-final
KAIST Business Modeling Analysis 기말 대체 과제 협업용 깃

# 협업 방식 (중요!!)
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
코드 전처리는 두가지 데이터 셋을 통해서 이루어짐
1. Clickstream dataset
    + 사람들이 몇 분동안, 어느 사이트에 방문했는지에 대한 기록
    + 자세한 사항은 [click-stream 설명](click_stream/click_stream.md) 참조
2. Querystring dataset
    + 사람들이 어떤 검색을, 몇 번 했는지에 대한 기록
    + 자세한 사항은 [query-string 설명](query_string/query_string.md) 참조

# 학습 및 모델링, 결과 보고
모델링은 Click-Stream dataset과 Query-String dataset 두개를 바탕으로 이루어짐
+ 자세한 사항은 [모델링 설명](modeling/modeling.md) 참조

# 코드를 구현할 때 주의 사항
> git을 다운받는다고 해서 코드가 모두 돌아가지 않으므로, 다음 지시를 따라야함
1. train, test 셋 내려받기
2. 경돈에게 model.pkl 받아 query_string 안에 저장
3. 각 train, test 셋을 모두 click_stream, query_string 폴더 안에 저장
4. 그 후 query_string.ipynb, click_stream.ipynb의 셀 모두 실행
5. 각 데이터 셋에서 도출한 preprocess_test.csv를 modeling 폴더 안에 저장
6. prediction.ipynb의 셀을 실행