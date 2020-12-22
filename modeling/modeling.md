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

# Modeling에서 고민했던 점
## Outcome Imbalance Problem
각 GROUP에 대해서 사람들의 비율이 불균형함
| GROUP TYPE | COUNT |
|------------|-------|
| 20대 여성    | 241   |
| 30대 여성    |  349  |
| 40대 여성    |  324  |
| 20대 남성    | 233   |
| 30대 남성    |  610  |
| 40대 남성    |  743  |

### (Normal)Sampling vs Undersampling vs Oversampling
+ Sampling을 할 경우, 20대 남성 대비 40대 남성에 더 많은 가중치가 부여 될 것으로 예상됨. Classification의 문제에서, 불균형 문제를 통해 특정 parameter가 비정상적으로 가중치가 높아지는 경우를 막고자 각 sample의 수를 한정짓는 method를 사용
+ `Undersampling`
    + 데이터를 가장 낮은 그룹에 맞추어 랜덤하게 제거하는 방법론
    + 다만, 원래 데이터가 2,500개 정도로 터무니 없이 작기에 undersampling을 사용하면 sample의 representativeness가 줄어듦
+ `Oversampling`
    + 데이터를 가장 높은 그룹에 맞추어 랜덤하게 복원추출하는 방법론
    + 보편적으로 사용하는 방법이나, sample의 bias가 증가할 가능성이 있음
+ 위 두가지 sampling을 통해 측정한 확률은 더 이상 확률의 의미를 가지지 않으나, 각 예측값에 대한 확률의 순서가 보존되기 때문에 보편적으로 사용될 수 있음

### Sequentially Prediction
+ 확률론적으로, 성별과 나이는 서로 독립적임 (i.e. 무관함)
+ 따라서, 성별에 대한 확률과 나이에 대한 확률을 측정한 뒤 서로 곱하면 GROUP에 대한 확률을 측정 가능
+ 각 확률을 측정하는데 있어 sample의 size가 한 번에 구하는 것 대비 크기 때문에 각 확률 측정에 있어서 sample 손실이 덜 할 것으로 예측
+ 그러나, Auto ML의 시간적 문제로 인해 시간 내에 시행할 지는 미지수