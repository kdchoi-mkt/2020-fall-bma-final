import pandas as pd
import pickle as pkl
import numpy as np
import urllib
from sklearn.cluster import KMeans

# Main Functions

def keyword_preprocess(file_name: str = './train_searchkeywords.tab') -> pd.DataFrame:
    """키워드 서치 데이터를 불러와서 전처리를 합니다. 

    전처리 스텝은 다음과 같습니다.
    1. 서치 데이터 정제 및 간단한 변수 부여
    3. Word 2 Vec을 이용한 라벨링 부여
    """

    data_frame = read_keyword(file_name)
    data_frame = construct_simple_variable(data_frame)
    data_frame = labeling_with_word_2_vec(data_frame)

    return data_frame    

def aggregate_keyword_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    keyword_gp = data_frame.groupby(['CUS_ID', "labels"])
    object_column = [
        'TOTAL_SEARCH_COUNT',
        'UNIQUE_SEARCH_COUNT',
        'WORD_LENGTH_AVG_AT_ONCE',
        'WORD_COUNT_AVG_AT_ONCE',
    ]
    
    cross_sectional_data = pd.DataFrame(data = [
                                            keyword_gp['QRY_CNT'].sum(),
                                            keyword_gp['KEYWORD'].nunique(),
                                            keyword_gp['WORD_LEN'].mean(),
                                            keyword_gp['WORD_COUNT'].mean()
                                        ],
                                        index = object_column)\
                             .transpose()\
                             .reset_index()

    for col in object_column:
        col_df = pd.pivot_table(
                        cross_sectional_data, 
                        index = 'CUS_ID', 
                        columns = ['labels'], 
                        values = [
                            col
                        ]
                    )[col]
        col_df_col = col_df.columns
        col_df.columns = [f"{col}_FOR_LABEL_{label}" for label in col_df_col]

        try:
            total_df = total_df.join(col_df)
        except:
            total_df = col_df

    return total_df

# Step Functions

def read_keyword(file_name: str = './train_searchkeywords.tab') -> pd.DataFrame:
    """키워드 서치 데이터를 불러옵니다."""
    return pd.read_table(file_name, encoding = 'cp949')

def construct_simple_variable(data_frame: pd.DataFrame) -> pd.DataFrame:
    """키워드 서치 데이터를 불러와서 기초 변수를 만드는 함수입니다."""
    KEYWORD_COL = 'KEYWORD'

    data_frame[KEYWORD_COL] = data_frame['QRY_STR'].apply(lambda x: _query_string_refinement(x))
    data_frame['WORD_LEN'] = data_frame[KEYWORD_COL].apply(len)
    data_frame['WORD_SPLIT'] = data_frame[KEYWORD_COL].apply(lambda x: x.split(' '))
    data_frame['WORD_COUNT'] = data_frame['WORD_SPLIT'].apply(lambda x: len(x))
    data_frame['SEARCH_ID'] = data_frame.index

    return data_frame

def labeling_with_word_2_vec(data_frame: pd.DataFrame) -> pd.DataFrame:
    """미리 학습된 모델 Word 2 Vec을 통해 각 키워드 서치의 특성을 라벨링합니다."""
    with open('model.pkl', 'rb') as f:
        model = pkl.load(f)
    
    data_frame['KEYWORD_VECTOR'] = data_frame['WORD_SPLIT'].apply(lambda x: _get_word_vector(model, x))
    data_frame = _clustering_word_vector(model, data_frame)
    data_frame = data_frame.drop(columns = ['KEYWORD_VECTOR'])

    return data_frame

# Private Functions

def _clustering_word_vector(model, data_frame: pd.DataFrame, n_clusters: int = 40) -> pd.DataFrame:
    """model을 통해서 클러스터링을 합니다."""
    kmeans = KMeans(n_clusters = n_clusters)
    kmeans.fit(model.wv[model.wv.vocab])

    word_vector_lists = np.concatenate(data_frame['KEYWORD_VECTOR'])\
                          .reshape(len(data_frame), 1000)\
                          .astype('float32')

    data_frame['labels'] = kmeans.predict(word_vector_lists)
    zero_vector_cond = data_frame['KEYWORD_VECTOR'].apply(lambda x: np.array_equal(x, np.zeros(1000)))
    data_frame.loc[zero_vector_cond, 'labels'] = -1

    return data_frame

def _query_string_refinement(query_str: str) -> str:
    """
    Return
    ======
    &query in string => return something
    else => return the first word
    """
    if '&query' not in query_str:
        return query_str.split('&')[0]
    return urllib.parse.parse_qs(query_str)['query'][0]

def _get_word_vector(model, word_list: list):
    """단어 리스트를 input으로 받으면, 그 서치에 대한 벡터를 output으로 뱉는다.
    
    Warning
    =======
    만약 `word_list`가 기존 단어장에 없다면, zero vector로 치환한다.
    """
    whole_word = np.zeros(1000)
    for word in word_list:
        try:
            word_vec = model.wv.get_vector(word)
            whole_word += word_vec
        except:
            pass
    return whole_word

if __name__ == '__main__':
    query_string = keyword_preprocess()
    cross_sectional = aggregate_keyword_data(query_string)
    cross_sectional.to_csv('./keyword_preprocess.csv')