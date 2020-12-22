# Prerequisite
모델링을 하기 전, 
+ `click_stream` 폴더 안의 `click_stream.py`를, 
+ `query_string` 폴더 안의 `query_string.py`를, 
+ `profile` 폴더 안의 `profile.py`를

실행시켜 나온 csv 파일을 `modeling` 폴더에 옮김

# Modeling 개요
1. clickstream, querystring, profile 학습 데이터를 `CUS_ID`를 통해 합침
    + 여기서 우리가 예측하는 것은 `GROUP` 데이터
2. AutoML을 이용하여 변수 최종 처리 및 모델 선택, 하이퍼 파라미터 튜닝 실시
    + 여기서 사용한 AutoML은 pycaret 모듈
    + 또한, Log Loss function을 이용하여 모델의 적합도 측정 및 튜닝 시행 
3. 최종 튜닝 후, test 데이터에 대해서 prediction 시행, 그 후 제출