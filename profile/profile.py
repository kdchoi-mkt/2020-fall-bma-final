import pandas as pd

age = { 
    10 : 20,
    20 : 20,
    30 : 30,
    40 : 40,
    50 : 40,
    60 : 40
}

def get_target(profile):
    """
    Return GROUP,GENDER,AGE_new
    """
    profile["AGE"] = profile["AGE"].apply(lambda x: age[x])
    return profile[['GENDER', 'AGE', 'GROUP']]


profile = pd.read_excel("train_profiles.xlsx")\
            .set_index("CUS_ID")

get_target(profile).to_csv('profile_preprocess.csv')