#%%
import pandas as pd
import sys
sys.path.append('../')
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data,gender_data
import seaborn as sns
import matplotlib.pyplot as plt


# %%
df_diabetes=processed_diabetes_data()
gender_df=gender_data()
df = pd.merge(df_diabetes, gender_df, on='sequence_no', how='inner')

# %%
df=df.dropna()
gender_map = {1.0: 'Male', 2.0: 'Female'}
df['gender'] = df['gender'].map(gender_map)
total_counts = len(df[df['EverTold_Diabetes'] == 1.0])
diabetic_counts = df[df['EverTold_Diabetes'] == 1.0].groupby('gender').size()
percent_diabetic = (diabetic_counts / total_counts) * 100
print(percent_diabetic)
# %%
diabetic_ages = df[df['EverTold_Diabetes'] == 1.0]['age']
non_diabetic_ages = df[df['EverTold_Diabetes'] == 2.0]['age']
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1) 
plt.hist(diabetic_ages, bins=10, alpha=0.7, color='red', edgecolor='black',density=True)
plt.title('Age Distribution of Diabetic Patients')
plt.xlabel('Age')
plt.ylabel('Density')
plt.subplot(1, 2, 2)
plt.hist(non_diabetic_ages, bins=10, alpha=0.7, color='green', edgecolor='black',density=True)
plt.title('Age Distribution of Non-Diabetic Patients')
plt.xlabel('Age')
plt.ylabel('Density')
plt.tight_layout()
plt.savefig('E:/sem5/datathon/images/age_distribution.png')
plt.show()
# %%
diabetic_males = df[(df['EverTold_Diabetes'] == 1) & (df['gender'] == 'Male')]['age']
diabetic_females = df[(df['EverTold_Diabetes'] == 1) & (df['gender'] == 'Female')]['age']
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)  
plt.hist(diabetic_males, bins=10, alpha=0.7, color='blue', edgecolor='black')
plt.title('Age Distribution of Diabetic Males')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.subplot(1, 2, 2)
plt.hist(diabetic_females, bins=10, alpha=0.7, color='orange', edgecolor='black')
plt.title('Age Distribution of Diabetic Females')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('E:/sem5/datathon/images/age_gender_distribution.png')
plt.show()
# %%
