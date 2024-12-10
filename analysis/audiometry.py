#%%
import pandas as pd
import sys
sys.path.append('../')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data,gender_data
import seaborn as sns
import matplotlib.pyplot as plt

#%%
dataset_path='../raw_datasets'
df=pd.read_sas(f'{dataset_path}/audiometry.XPT', format='xport')

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
df_have_diabetes=pd.merge(df_have_diabetes, gender_df, on='sequence_no', how='inner')
df_nothave_diabetes=pd.merge(df_nothave_diabetes, gender_df, on='sequence_no', how='inner')
gender_map = {1.0: 'Male', 2.0: 'Female'}
df_have_diabetes['gender'] = df_have_diabetes['gender'].map(gender_map)
df_nothave_diabetes['gender'] = df_nothave_diabetes['gender'].map(gender_map)
# %%
df_have_diabetes=df_have_diabetes.dropna(subset=['HearingStatus_NoAid'])
df_nothave_diabetes=df_nothave_diabetes.dropna(subset=['HearingStatus_NoAid'])
df_have_diabetes=df_have_diabetes[df_have_diabetes['HearingStatus_NoAid']<10]
df_nothave_diabetes=df_nothave_diabetes[df_nothave_diabetes['HearingStatus_NoAid']<10]
df_have_diabetes['group']='Diabetic'
df_nothave_diabetes['group']='Non-Diabetic'
# %%
sns.set(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.countplot(data=df_have_diabetes, x='HearingStatus_NoAid', ax=axes[0], palette='Blues')
axes[0].set_title('Hearing Condition of Diabetic Patients')
axes[0].set_xlabel('General condition of hearing')
axes[0].set_ylabel('Count')
sns.countplot(data=df_nothave_diabetes, x='HearingStatus_NoAid', ax=axes[1], palette='Reds')
axes[1].set_title('Hearing Condition of Non-Diabetic Patients')
axes[1].set_xlabel('General condition of hearing')
axes[1].set_ylabel('Count')

categories = {
    1: "Excellent",
    2: "Good",
    3: "A little trouble",
    4: "Moderate hearing trouble",
    5: "A lot of trouble",
    6: "Deaf"
}
handles = [plt.Line2D([0], [0], marker='o', color='w', label=f'{key}: {value}', 
                       markerfacecolor='gray') for key, value in categories.items()]
fig.legend(handles=handles, title="Categories", loc='upper right', bbox_to_anchor=(1.15, 1), fontsize='medium')
plt.tight_layout()
plt.savefig("E:/sem5/datathon/images/hearing_condition.png")
plt.show()
# %%
