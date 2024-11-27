#%%
import pandas as pd
import sys
sys.path.append('../')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data,gender_data
import seaborn as sns
import matplotlib.pyplot as plt

# %%
dataset_path='../raw_datasets'
df=pd.read_sas(f'{dataset_path}/smoking_cigarette_use.XPT', format='xport')

# %%
mapping=get_variable_names()
df=rename_columns(df, mapping)
df_diabetes=processed_diabetes_data()
gender_df=gender_data()
# %%
seq_have_diabetes = df_diabetes[df_diabetes['EverTold_Diabetes']==1.0]['sequence_no']
seq_nothave_diabetes = df_diabetes[df_diabetes['EverTold_Diabetes']==2.0]['sequence_no']
df_have_diabetes = df[df['sequence_no'].isin(seq_have_diabetes)]
df_nothave_diabetes = df[df['sequence_no'].isin(seq_nothave_diabetes)]
df_have_diabetes = pd.merge(df_have_diabetes, gender_df, on='sequence_no', how='inner')
gender_map = {1.0: 'Male', 2.0: 'Female'}
df_have_diabetes['gender'] = df_have_diabetes['gender'].map(gender_map)
df_nothave_diabetes = pd.merge(df_nothave_diabetes, gender_df, on='sequence_no', how='inner')
df_nothave_diabetes['gender'] = df_nothave_diabetes['gender'].map(gender_map)
df_have_diabetes=df_have_diabetes.dropna(subset=['CurrentCigaretteSmoking'])
df_nothave_diabetes=df_nothave_diabetes.dropna(subset=['CurrentCigaretteSmoking'])

# %%
grouped_diabetes=df_have_diabetes.groupby(['CurrentCigaretteSmoking'])['sequence_no'].count()/df_have_diabetes['sequence_no'].count()
grouped_notdiabetes=df_nothave_diabetes.groupby(['CurrentCigaretteSmoking'])['sequence_no'].count()/df_nothave_diabetes['sequence_no'].count()
print(grouped_diabetes)
print(grouped_notdiabetes)
# %%
