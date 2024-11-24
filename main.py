#%%
import pandas as pd
import sys
sys.path.append('./')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data

#%%
dataset_path='raw_datasets'
df=pd.read_sas(f'{dataset_path}/weight_history.XPT', format='xport')

# %%
mapping=get_variable_names()
df=rename_columns(df, mapping)

# %%
df_diabetes=processed_diabetes_data()

# %%
seq_have_diabetes = df_diabetes[df_diabetes['EverTold_Diabetes']==1.0]['sequence_no']
seq_nothave_diabetes = df_diabetes[df_diabetes['EverTold_Diabetes']==2.0]['sequence_no']
# %%
df_have_diabetes = df[df['sequence_no'].isin(seq_have_diabetes)]
df_nothave_diabetes = df[df['sequence_no'].isin(seq_nothave_diabetes)]

df_have_diabetes = df_have_diabetes.dropna(subset=['CurrentHeight', 'CurrentWeight','WeightOneYearAgo'])
df_nothave_diabetes = df_nothave_diabetes.dropna(subset=['CurrentHeight', 'CurrentWeight','WeightOneYearAgo'])

df_have_diabetes["weight_change"] = df_have_diabetes["CurrentWeight"]-df_have_diabetes['WeightOneYearAgo']
df_nothave_diabetes["weight_change"] = df_nothave_diabetes["CurrentWeight"]-df_nothave_diabetes['WeightOneYearAgo']

df_have_diabetes["bmi"] = df_have_diabetes["CurrentWeight"]/(df_have_diabetes['CurrentHeight']**2)
df_nothave_diabetes["bmi"] = df_nothave_diabetes["CurrentWeight"]/(df_nothave_diabetes['CurrentHeight']**2)


# %%
q1_bmi_have_diabetes = df_have_diabetes["bmi"].quantile(0.25)
q3_bmi_have_diabetes = df_have_diabetes["bmi"].quantile(0.75)
print(f'For Diabetes, BMI - Q1: {q1_bmi_have_diabetes} and Q3: {q3_bmi_have_diabetes}')

q1_bmi_nothave_diabetes = df_nothave_diabetes["bmi"].quantile(0.25)
q3_bmi_nothave_diabetes = df_nothave_diabetes["bmi"].quantile(0.75)
print(f'For Non-Diabetes, BMI - Q1: {q1_bmi_nothave_diabetes} and Q3: {q3_bmi_nothave_diabetes}')
# %%

q1_weightchange_have_diabetes = df_have_diabetes["weight_change"].quantile(0.25)
q3_weightchange_have_diabetes = df_have_diabetes["weight_change"].quantile(0.75)
print(f'For Diabetes, Weight Change - Q1: {q1_weightchange_have_diabetes} and Q3: {q3_weightchange_have_diabetes}')

q1_weightchange_nothave_diabetes = df_nothave_diabetes["weight_change"].quantile(0.25)
q3_weightchange_nothave_diabetes = df_nothave_diabetes["weight_change"].quantile(0.75)
print(f'For Non-Diabetes, Weight Change - Q1: {q1_weightchange_nothave_diabetes} and Q3: {q3_weightchange_nothave_diabetes}')
# %%

yes_diabetes_try=df_have_diabetes["TriedToLoseWeight_Past12Months"]
yes_nodiabetes_try=df_nothave_diabetes["TriedToLoseWeight_Past12Months"]

yesdia_yes=0
yesdia_no=0
nodia_yes=0
nodia_no=0
for i in yes_diabetes_try:
    if(i==1.0):
        yesdia_yes+=1
    else:
        yesdia_no+=1

for i in yes_nodiabetes_try:
    if(i==1.0):
        nodia_yes+=1
    else:
        nodia_no+=1
# %%
print(f'For Diabetes, Tried to Lose Weight - Yes: {yesdia_yes} and No: {yesdia_no}. Percentage: {yesdia_yes/(yesdia_yes+yesdia_no)}')
print(f'For Non-Diabetes, Tried to Lose Weight - Yes: {nodia_yes} and No: {nodia_no}. Percentage: {nodia_yes/(nodia_yes+nodia_no)}')
# %%
