#%%
import pandas as pd
import sys
sys.path.append('./')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data

#%%
dataset_path='raw_datasets'
df=pd.read_sas(f'{dataset_path}/diabetes.XPT', format='xport')

# %%
mapping=get_variable_names()
df=rename_columns(df, mapping)

# %%
df_diabetes=processed_diabetes_data()