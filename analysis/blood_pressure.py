#%%
import pandas as pd
import sys
sys.path.append('../')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data,bar_with_percentage
import seaborn as sns
import matplotlib.pyplot as plt

#%%
dataset_path='../raw_datasets'
df=pd.read_sas(f'{dataset_path}/blood_pressure_cholesterol.XPT', format='xport')

# %%
mapping=get_variable_names()
df=rename_columns(df, mapping)
df_diabetes=processed_diabetes_data()

# %%
seq_have_diabetes = df_diabetes[df_diabetes['EverTold_Diabetes']==1.0]['sequence_no']
seq_nothave_diabetes = df_diabetes[df_diabetes['EverTold_Diabetes']==2.0]['sequence_no']
df_have_diabetes = df[df['sequence_no'].isin(seq_have_diabetes)]
df_nothave_diabetes = df[df['sequence_no'].isin(seq_nothave_diabetes)]

# %%
yes_diabetes_bp=df_have_diabetes["CurrentlyTaking_BloodPressureMedication"].dropna()
yes_diabetes_bp_proportion=yes_diabetes_bp[yes_diabetes_bp<3].value_counts(normalize=True).sort_index()
print("People with diabetes who are taking blood pressure medication: ")
print(yes_diabetes_bp_proportion)

no_diabetes_bp=df_nothave_diabetes["CurrentlyTaking_BloodPressureMedication"].dropna()
no_diabetes_bp=no_diabetes_bp[no_diabetes_bp<3].value_counts(normalize=True).sort_index()
print("People without diabetes who are taking blood pressure medication: ")
print(no_diabetes_bp)

# %%
yes_diabetes_high_bp=df_have_diabetes["EverTold_Hypertension"].dropna()
yes_diabetes_high_bp=yes_diabetes_high_bp[yes_diabetes_high_bp<3]
no_diabetes_high_bp=df_nothave_diabetes["EverTold_Hypertension"].dropna()
no_diabetes_high_bp=no_diabetes_high_bp[no_diabetes_high_bp<3]
df1_high_bp = pd.DataFrame({'value': yes_diabetes_high_bp, 'group': 'Having Diabetes'})
df2_high_bp = pd.DataFrame({'value': no_diabetes_high_bp, 'group': 'Not Having Diabetes'})

df_high_bp = pd.concat([df1_high_bp, df2_high_bp], ignore_index=True)

counts = df_high_bp.groupby(['group', 'value']).size().unstack()
percentages = counts.div(counts.sum(axis=1), axis=0) * 100
bar_with_percentage(percentages,'Ever told about high blood pressure','ever_told_high_bp')

# %%
print("Proportion of people with diabetes who had ever told about high blood pressure: ")
print(df1_high_bp.value_counts(normalize=True).sort_index())

print("Proportion of people without diabetes who had ever told about high blood pressure: ")
print(df2_high_bp.value_counts(normalize=True).sort_index())
#%%
yes_diabetes_confirmed_high_bp=df_have_diabetes["ConfirmedHypertension_Visits"].dropna()
yes_diabetes_confirmed_high_bp=yes_diabetes_confirmed_high_bp[yes_diabetes_confirmed_high_bp<3]
no_diabetes_confirmed_high_bp=df_nothave_diabetes["ConfirmedHypertension_Visits"].dropna()
no_diabetes_confirmed_high_bp=no_diabetes_confirmed_high_bp[no_diabetes_confirmed_high_bp<3]

print("Proportion of people with diabetes who had ever told about high blood pressure: ")
print(yes_diabetes_confirmed_high_bp.value_counts(normalize=True).sort_index())

print("Proportion of people without diabetes who had ever told about high blood pressure: ")
print(no_diabetes_confirmed_high_bp.value_counts(normalize=True).sort_index())


# %%
yes_diabetes_high_cholesterol=df_have_diabetes["EverTold_HighCholesterol"].dropna()
yes_diabetes_high_cholesterol=yes_diabetes_high_cholesterol[yes_diabetes_high_cholesterol<3]
no_diabetes_high_cholesterol=df_nothave_diabetes["EverTold_HighCholesterol"].dropna()
no_diabetes_high_cholesterol=no_diabetes_high_cholesterol[no_diabetes_high_cholesterol<3]
df1_high_cholesterol = pd.DataFrame({'value': yes_diabetes_high_cholesterol, 'group': 'Having Diabetes'})
df2_high_cholesterol = pd.DataFrame({'value': no_diabetes_high_cholesterol, 'group': 'Not Having Diabetes'})

df_high_cholesterol = pd.concat([df1_high_cholesterol, df2_high_cholesterol], ignore_index=True)

counts = df_high_cholesterol.groupby(['group', 'value']).size().unstack()
percentages2 = counts.div(counts.sum(axis=1), axis=0) * 100
percentages2.plot(kind='bar', stacked=True)
bar_with_percentage(percentages2,'Ever told about high cholesterol','ever_told_high_cholesterol')
# %%
