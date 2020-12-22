import pandas as pd

def merging_all_information(click_stream_file, query_string_file, demographic_file):
    click_stream_df = pd.read_csv(click_stream_file)
    query_string_df = pd.read_csv(query_string_file)
    demographic_df = pd.read_csv(demographic_file)