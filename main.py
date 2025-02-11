#%%
import pandas as pd
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data, gender_data
from functools import reduce

#%%
def read_file(filename=''):

    dataset_path='raw_datasets'
    df=pd.read_sas(f'{dataset_path}/{filename}.XPT', format='xport')
    mapping=get_variable_names()
    df=rename_columns(df, mapping)  
    
    return df

#%%
df_diabetes=processed_diabetes_data()  #Taken data of people which give answer as yes or no
df_gender=gender_data()
df_audio=read_file('audiometry')
df_blood_pressure=read_file('blood_pressure_cholesterol')
df_general_health=read_file('hospital_utilization_access_to_care')
df_weight=read_file('weight_history')
df_occupation=read_file('occupation')

#%%
dataframes = [df_diabetes,df_gender, df_audio, df_blood_pressure, df_general_health, df_weight, df_occupation]
df = reduce(lambda left, right: pd.merge(left, right, on='sequence_no', how='inner'), dataframes)

# %%
columns_to_select = ['sequence_no', 'EverTold_Diabetes', 'gender', 'age', 'income','HearingStatus_NoAid','EverTold_Hypertension','EverTold_HighCholesterol','GeneralHealth_Status','CurrentHeight','CurrentWeight','WorkExperience_LastWeek','WeightOneYearAgo']
df=df[columns_to_select]

# Total=8223,  after dropping all NA= 6829
# dropping rows with >1 NAN values= 8210
# dropping rows with >2 NAN values= 8211

# Column wise nan values count
# sequence_no                    0
# EverTold_Diabetes              0
# gender                         0
# age                            0
# income                      1393
# HearingStatus_NoAid            0
# EverTold_Hypertension          0
# EverTold_HighCholesterol       0
# GeneralHealth_Status           0
# CurrentHeight                 12
# CurrentWeight                 12
# WorkExperience_LastWeek       13
# WeightOneYearAgo              12

#%%
