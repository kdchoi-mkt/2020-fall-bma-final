import pandas as pd
from constants import WEEKDAY_DICT, MONTH_DICT
from datetime import datetime

def click_stream_preprocess(file_name: str = './train_clickstreams.tab') -> pd.DataFrame:
    """Clickstream 데이터를 전처리합니다.

    전처리 스텝은 다음과 같습니다.
    1. 시간 데이터 전처리
    2. 각 사이트에 대해서 접속 순위를 10 분위로 매김
    3. 사이트 방문 횟수, 잔류 시간에 대해서 변수화
    """
    data_frame = read_click_stream(file_name)
    data_frame = preprocess_time_column(data_frame)
    data_frame = construct_qtile(data_frame, nbins = 10)

    # 각 아이디별 접속횟수기반
    site_data_frame_list = list()
    site_data_frame_list.append(
        aggregate_and_get_group_by(data_frame, 'SITE_CNT', ['CUS_ID'], agg_func = 'mean')
    )
    site_data_frame_list.append(
        aggregate_and_get_group_by(data_frame, 'SITE_CNT', ['CUS_ID'], agg_func = 'sum')
    )
    site_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'SITE_CNT', ['CUS_ID', 'MONTH'], agg_func = 'mean')
    )
    site_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'SITE_CNT', ['CUS_ID', 'MONTH'], agg_func = 'sum')
    )
    site_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'SITE_CNT', ['CUS_ID', 'WEEKDAY'], agg_func = 'mean')
    )
    site_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'SITE_CNT', ['CUS_ID', 'WEEKDAY'], agg_func = 'sum')
    )
    # 각 아이디별 체류시간 기반
    duration_data_frame_list = list()
    duration_data_frame_list.append(
        aggregate_and_get_group_by(data_frame, 'ST_TIME', ['CUS_ID'], agg_func = 'mean')
    )
    duration_data_frame_list.append(
        aggregate_and_get_group_by(data_frame, 'ST_TIME', ['CUS_ID'], agg_func = 'sum')
    )
    duration_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'ST_TIME', ['CUS_ID', 'MONTH'], agg_func = 'mean')
    )
    duration_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'ST_TIME', ['CUS_ID', 'MONTH'], agg_func = 'sum')
    )
    duration_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'ST_TIME', ['CUS_ID', 'WEEKDAY'], agg_func = 'mean')
    )
    duration_data_frame_list.append(
        aggregate_and_get_pivot(data_frame, 'ST_TIME', ['CUS_ID', 'WEEKDAY'], agg_func = 'sum')
    )
    total_data_frame = pd.DataFrame()
    
    return total_data_frame.join(site_data_frame_list, how = 'outer')\
                           .join(duration_data_frame_list, how = 'outer')\
                           .fillna(0)

def read_click_stream(file_name) -> pd.DataFrame:
    """클릭스트림 데이터를 읽는다."""
    return pd.read_table(file_name, encoding = 'cp949')\
             .dropna()

# 시간 전처리
def preprocess_time_column(data_frame: pd.DataFrame)-> pd.DataFrame:
    """
    step 1. (int)time to datetime
    step 2. make weekday column
    step 3. make month column
    """
    data_frame['TIME_ID'] = data_frame['TIME_ID'].astype(str).apply(lambda x: datetime.strptime(x, '%Y%m%d%H'))
    
    data_frame["WEEKDAY"]= data_frame["TIME_ID"].dt\
                                                .weekday\
                                                .apply(lambda x: WEEKDAY_DICT[x])
    
    data_frame["MONTH"] = data_frame["TIME_ID"].dt\
                                               .month\
                                               .apply(lambda x: MONTH_DICT[x])
    
    return data_frame

# 주요 사이트 방문횟수로 10분위
def construct_qtile(df, nbins, group_col = 'SITE', agg_col = 'SITE_CNT'):
    """construct quantile based on SITE_CNT"""
    labels = range(nbins, 0, -1)

    ex = df.groupby([group_col])[[agg_col]].sum().reset_index()
    
    ex[f"QTILE_{nbins}"] = pd.qcut(ex[agg_col], nbins + 2,
                          labels=labels, duplicates='drop')
    
    ex = ex.drop(columns = [agg_col])
    
    return pd.merge(df, ex, on=group_col)

def aggregate_and_get_pivot(df, target_column, group_columns, agg_func = 'mean'):
    """Transform panel data into cross-sectional data"""
    df_gp = df.groupby(group_columns)[[target_column]]
    new_target_column = f"{target_column}_{agg_func}"

    if agg_func == 'mean':
        objection = df_gp.mean()
    elif agg_func == 'sum':
        objection = df_gp.sum()
    else:
        raise ValueError("Wrong")

    objection = objection.reset_index()\
                            .rename(columns = {target_column: new_target_column})

    pivot_table = pd.pivot_table(objection,
                                    index = group_columns[0],
                                    columns = [group_columns[1]],
                                    values = [new_target_column])[new_target_column]

    pivot_table.columns = [f"{new_target_column}_{value}" for value in pivot_table.columns]
        
    return pivot_table

def aggregate_and_get_group_by(df, target_column, group_columns, agg_func = 'mean'):
    df_gp = df.groupby(group_columns)[target_column]
    new_target_column = f"{target_column}_{agg_func}"
    
    if agg_func == 'mean':
        objection = df_gp.mean()
    elif agg_func == 'sum':
        objection = df_gp.sum()
    else:
        raise ValueError("Wrong")

    objection = objection.reset_index()\
                         .rename(columns = {target_column: new_target_column})

    return objection.set_index('CUS_ID')
    