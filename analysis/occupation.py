#%%
import pandas as pd
import sys
sys.path.append('../')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data,gender_data
import seaborn as sns
import matplotlib.pyplot as plt

#%%
dataset_path='../raw_datasets'
df=pd.read_sas(f'{dataset_path}/occupation.XPT', format='xport')

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

#%%
yes_diabetes_work=df_have_diabetes["WorkExperience_LastWeek"].dropna()
yes_diabetes_work=yes_diabetes_work[yes_diabetes_work<5]
no_diabetes_work=df_nothave_diabetes["WorkExperience_LastWeek"].dropna()
no_diabetes_work=no_diabetes_work[no_diabetes_work<5]
df1_work = pd.DataFrame({'value': yes_diabetes_work, 'group': 'Having Diabetes'})
df2_work = pd.DataFrame({'value': no_diabetes_work, 'group': 'Not Having Diabetes'})

df_work = pd.concat([df1_work, df2_work], ignore_index=True)

plt.figure(figsize=(10, 6))
sns.violinplot(x='group', y='value', data=df_work)
plt.title('Violin Plot of Work')
plt.ylabel('Values')
textstr = (
    "Work Experience Categories:\n"
    "1: Working at a job or business\n"
    "2: With a job or business but not at work\n"
    "3: Looking for work\n"
    "4: Not working at a job or business"
)

props = dict(boxstyle='round', facecolor='white', alpha=0.8)
plt.text(
    1.05, 0.5, textstr, transform=plt.gca().transAxes,
    fontsize=10, verticalalignment='center', bbox=props
)
# plt.savefig('E:/sem5/datathon/images/work_experience.png')
plt.show()

#%%
df_have_diabetes['group'] = 'Having Diabetes'
df_nothave_diabetes['group'] = 'Not Having Diabetes'
df_age_work = pd.concat([df_have_diabetes, df_nothave_diabetes], ignore_index=True)
df_age_work = df_age_work[['WorkExperience_LastWeek', 'age', 'group','gender']].dropna()
df_age_work = df_age_work[df_age_work['WorkExperience_LastWeek'] < 5]
work_experience_labels = {
    1: 'Working at a job or business',
    2: 'With a job or business but not at work',
    3: 'Looking for work',
    4: 'Not working at a job or business'
}
df_age_work['WorkExperience_LastWeek'] = df_age_work['WorkExperience_LastWeek'].map(work_experience_labels)
plt.figure(figsize=(12, 8))
sns.boxplot(
    x='WorkExperience_LastWeek',
    y='age',
    hue='group',
    data=df_age_work,
    palette={'Having Diabetes': 'red', 'Not Having Diabetes': 'blue'}
)
plt.title('Age Distribution by Work Experience Categories and Diabetes Status', fontsize=14)
plt.xlabel('Work Experience Categories', fontsize=12)
plt.ylabel('Age', fontsize=12)
plt.xticks(rotation=20)
plt.legend(title='Group', loc='upper right')
# plt.savefig('E:/sem5/datathon/images/age_work_experience.png')
plt.show()

# %%
g = sns.FacetGrid(
    df_age_work, 
    row="gender", 
    col="group", 
    height=5, 
    aspect=1.4, 
    sharey=True
)
g.map_dataframe(
    sns.boxplot, 
    x="WorkExperience_LastWeek", 
    y="age",
    order=[
        "Working at a job or business", 
        "With a job or business but not at work", 
        "Looking for work", 
        "Not working at a job or business"
    ]
)
for ax in g.axes.flat:
    ax.set_xticklabels(
        ["Working at a job", "With a job (not working)", "Looking for work", "Not working"],
        rotation=20
    )
g.set_axis_labels("Work Experience Categories", "Age")
g.set_titles("{row_name} Gender | {col_name}")
plt.subplots_adjust(top=0.9)
g.fig.suptitle("Age Distribution by Work Experience, Diabetes Status, and Gender", fontsize=16)
plt.savefig("E:/sem5/datathon/images/age_work_experience_gender.png")
plt.show()


#%%
yes_diabetes_workhrs=df_have_diabetes["HoursWorked_LastWeek"].dropna()
yes_diabetes_workhrs=yes_diabetes_workhrs[yes_diabetes_workhrs<1000]
no_diabetes_workhrs=df_nothave_diabetes["HoursWorked_LastWeek"].dropna()
no_diabetes_workhrs=no_diabetes_workhrs[no_diabetes_workhrs<1000]

print(yes_diabetes_workhrs.describe())
print(no_diabetes_workhrs.describe())

df1_hrs = pd.DataFrame({'value': yes_diabetes_workhrs, 'group': 'Having Diabetes'})
df2_hrs = pd.DataFrame({'value': no_diabetes_workhrs, 'group': 'Not Having Diabetes'})

df_hrs = pd.concat([df1_hrs, df2_hrs], ignore_index=True)

plt.figure(figsize=(12, 6))
sns.violinplot(x='group', y='value', data=df_hrs)
plt.title('Violin Plot of Work Hours')
plt.ylabel('Hours')
plt.savefig('E:/sem5/datathon/images/working_hours.png')
plt.show()

# %%
yes_diabetes_notworking_reason=df_have_diabetes["MainReasonNotWorking_LastWeek"].dropna()
yes_diabetes_notworking_reason=yes_diabetes_notworking_reason[yes_diabetes_notworking_reason<10]
no_diabetes_notworking_reason=df_nothave_diabetes["MainReasonNotWorking_LastWeek"].dropna()
no_diabetes_notworking_reason=no_diabetes_notworking_reason[no_diabetes_notworking_reason<10]
df1_reason = pd.DataFrame({'value': yes_diabetes_notworking_reason, 'group': 'Having Diabetes'})
df2_reason = pd.DataFrame({'value': no_diabetes_notworking_reason, 'group': 'Not Having Diabetes'})

df_reason = pd.concat([df1_reason, df2_reason], ignore_index=True)

plt.figure(figsize=(12, 6))
sns.violinplot(x='group', y='value', data=df_reason)
plt.title('Not Working last week reason')
plt.ylabel('Reason')
textstr = (
    "Reasons:\n"
    "1: Taking care of house or family\n"
    "2: Going to school\n"
    "3: Retired\n"
    "4: Unable to work for health reasons/Disabled\n"
    "5: Can't find work/On layoff\n"
    "6: Seasonal/Contract work\n"
    "7: Other"
)

props = dict(boxstyle='round', facecolor='white', alpha=0.8)
plt.text(
    1.05, 0.5, textstr, transform=plt.gca().transAxes,
    fontsize=10, verticalalignment='center', bbox=props
)
plt.savefig('E:/sem5/datathon/images/reason_not_working.png')
plt.show()

# %%

diabetes_health=0
for i in yes_diabetes_notworking_reason:
    if(i==4.0):
        diabetes_health+=1
print("Percentage of people with diabetes who are not working because of health issues: ",diabetes_health/len(yes_diabetes_notworking_reason)*100)

# %%
notdiabetes_health=0
for i in no_diabetes_notworking_reason:
    if(i==4.0):
        notdiabetes_health+=1
print("Percentage of people without diabetes who are not working because of health issues: ",notdiabetes_health/len(no_diabetes_notworking_reason)*100)

#%%
yes_diabetes_working_days=df_have_diabetes["DaysWorkingPerWeek"].dropna()
yes_diabetes_working_days=yes_diabetes_working_days[yes_diabetes_working_days<10]
no_diabetes_working_days=df_nothave_diabetes["DaysWorkingPerWeek"].dropna()
no_diabetes_working_days=no_diabetes_working_days[no_diabetes_working_days<10]
print(f"Average working days for people with diabetes in a week: {round(yes_diabetes_working_days.mean(),2)}")
print(f"Average working days for people without diabetes in a week: {round(no_diabetes_working_days.mean(),2)}")

# %%
