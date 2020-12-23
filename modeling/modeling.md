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

여러가지 방안 중, 이번 분석에서는 normal sampling과 oversampling 기법 두 가지에 대해서 모델을 설정한 뒤 `log loss`가 가장 적은 모델을 채택하는 것으로 방향을 정함

## Variable Selection Problem
+ Importance Variable Selection
    + 중요한 변수만 선택하여 모델의 계산 속도를 높이기 위함
+ Ignorance of Low Variable
    + 적은 변량을 가진 변수를 제거하여 overfitting 이슈를 막기 위함
+ Remove Multicollinearity
    + 다중공선성 문제로 인해 제대로 된 예측을 할 수 없는 이슈를 막기 위함

# Modeling with pycaret

pycaret 모듈에서 다음과 같은 변수 선택 기법을 이용하여 모델 비교 및 하이퍼 파라미터 튜닝을 진행

+ Importance Variable Selection
+ Ignorance of Low Variable
+ Remove Multicollinearity


## Normal Sampling: Random Forest

+ Random Forest
+ Ensemble method 중 하나로, N개의 decision tree로 구성됨
+ Input을 각 decision tree가 받아 도출한 값을 취함하여, 과반수가 넘는 값으로 output을 도출하는 기법

각 비율을 균일하게 맞추지 않고 현재 데이터 그대로 모델을 작성했을 경우에는 `Random Forest` 기법이 가장 퍼포먼스가 좋음 (`log loss`: 1.56)

그러나, `log loss` 기준 튜닝을 시도하였을 때 더 높아지는 (성능이 낮아지는) 현상이 있었기에, Random Forest를 사용한다면 튜닝 전의 모델이 채택될 것으로 예상됨

## Oversampling: CatBoost

+ CatBoost 
+ Ensemble method 중 하나로, 약한 분류기부터 시작하여 점차 성능을 높이는 기법
+ CatBoost에 대한 Loss function의 gradient를 이용하여 계산함
+ 특히, category variable을 가지고 있는 경우에 사용하기 용이함

각 비율을 균일하게 맞추고 모델을 구성한 경우에는 `CatBoost` 기법이 가장 퍼포먼스가 좋음 (`log loss`: 1.59)

또한, 위와 마찬가지로 튜닝을 시도하였을 때 성능이 더 낮아지는 현상이 있었기에, CatBoost를 사용한다면 튜닝 후의 모델이 채택될 것으로 예상됨

## Result

각 비율을 균일하게 맞추지 않는 경우가 `log loss`가 낮았기에, `Random Forest` 기법을 이용하여 prediction을 실시함. 

그러나, SMOTE 등의 oversampling을 사용하면 각 군에 대해 확률이 과대평가, 또는 과소평가 되기 때문에 더 이상 결과 값이 확률의 의미를 가지지는 않으므로 `log loss`가 항상 맞는 지표는 아님에 주의해야함
