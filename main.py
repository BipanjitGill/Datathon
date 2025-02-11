import argparse
import pandas as pd
import numpy as np
from utils.funcs import get_variable_names, rename_columns, processed_diabetes_data, demographic_data2
from functools import reduce
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import StackingClassifier,RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, AdaBoostClassifier
from sklearn.feature_selection import SelectKBest, f_classif, RFE
import optuna
import lightgbm as lgb
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE,RandomOverSampler
from imblearn.under_sampling import TomekLinks
from imblearn.combine import SMOTETomek
from imblearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, accuracy_score, make_scorer
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split, GridSearchCV
from sklearn.experimental import enable_iterative_imputer 
from sklearn.impute import IterativeImputer, KNNImputer
import xgboost as xgb
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

def read_file(filename=''):

    dataset_path='raw_datasets'
    df=pd.read_sas(f'{dataset_path}/{filename}.XPT', format='xport')
    mapping=get_variable_names()
    df=rename_columns(df, mapping)  
    threshold = int(0.7 * len(df))  
    df = df.dropna(axis=1, thresh=threshold)
    return df

df_diabetes=processed_diabetes_data()  
df_demographic=demographic_data2()
df_audio=read_file('audiometry')
df_blood_pressure=read_file('blood_pressure_cholesterol')
df_general_health=read_file('hospital_utilization_access_to_care')
df_weight=read_file('weight_history')
df_occupation=read_file('occupation')
df_sleep=read_file('sleep_disorders')
df_smoke1=read_file('smoking_cigarette_use')
df_phy_activity=read_file('physical_activity')
df_alcohol=read_file('alcohol_use')
dataframes = [df_diabetes,df_demographic, df_audio, df_blood_pressure, df_general_health, df_weight, df_occupation,df_sleep,df_smoke1,df_phy_activity,df_alcohol]
df = reduce(lambda left, right: pd.merge(left, right, on='sequence_no', how='inner'), dataframes)
columns_to_select = ['sequence_no', 'EverTold_Diabetes', 'race', 'gender', 'age','sample_weight','sample_weight2','HearingStatus_NoAid','EverTold_Hypertension','EverTold_HighCholesterol','CurrentlyTaking_CholesterolMedication','GeneralHealth_Status','CurrentHeight','CurrentWeight','WorkExperience_LastWeek','WeightOneYearAgo','SmokedAtLeast100CigarettesInLife','EverHad_Alcohol','SittingTime_TypicalDay','WeekdaySleepHours','AlcoholConsumptionFrequency_12Months','Duration_ModerateActivity_PerSession','Frequency_ModerateActivity']
df=df[columns_to_select]

df['EverHad_Alcohol'] = df['EverHad_Alcohol'].replace(7.0, 1.0)
df['AlcoholConsumptionFrequency_12Months'] = df['AlcoholConsumptionFrequency_12Months'].replace(77.0, 1.0)
df['AlcoholConsumptionFrequency_12Months'] = df['AlcoholConsumptionFrequency_12Months'].replace(99.0, 1.0)
df['EverTold_Hypertension'] = df['EverTold_Hypertension'].replace(9.0, 2.0)
df['EverTold_HighCholesterol'] = df['EverTold_HighCholesterol'].replace(9.0, 2.0)
df['CurrentlyTaking_CholesterolMedication'] = df['CurrentlyTaking_CholesterolMedication'].replace(9.0, 2.0)
df['GeneralHealth_Status'] = df['GeneralHealth_Status'].replace(9.0, 4.0)
df['Frequency_ModerateActivity'] = df['Frequency_ModerateActivity'].replace(9999.0, np.nan)
df['Frequency_ModerateActivity'] = df['Frequency_ModerateActivity'].replace(7777.0, np.nan)
df['Duration_ModerateActivity_PerSession'] = df['Duration_ModerateActivity_PerSession'].replace(7777.0, np.nan)
df['SmokedAtLeast100CigarettesInLife'] = df['SmokedAtLeast100CigarettesInLife'].replace(9.0, np.nan)
df['SmokedAtLeast100CigarettesInLife'] = df['SmokedAtLeast100CigarettesInLife'].replace(7.0, np.nan)
df['CurrentHeight'] = df['CurrentHeight'].replace(7777.0, np.nan)
df['CurrentHeight'] = df['CurrentHeight'].replace(9999.0, np.nan)
df['CurrentWeight'] = df['CurrentWeight'].replace(9999.0, np.nan)
df['CurrentWeight'] = df['CurrentWeight'].replace(7777.0, np.nan)
df['WeightOneYearAgo'] = df['WeightOneYearAgo'].replace(7777.0, np.nan)
df['WeightOneYearAgo'] = df['WeightOneYearAgo'].replace(9999.0, np.nan)
df['SittingTime_TypicalDay'] = df['SittingTime_TypicalDay'].replace(9999.0, np.nan)
df['SittingTime_TypicalDay'] = df['SittingTime_TypicalDay'].replace(7777.0, np.nan)
df['WorkExperience_LastWeek'] = df['WorkExperience_LastWeek'].replace(9.0, np.nan)

temp_df=df[['CurrentHeight','CurrentWeight','WeightOneYearAgo','Duration_ModerateActivity_PerSession','Frequency_ModerateActivity','age','SittingTime_TypicalDay','WeekdaySleepHours']]
imputer = IterativeImputer(random_state=0)
imputed_data = imputer.fit_transform(temp_df)
imputed_df = pd.DataFrame(imputed_data, columns=temp_df.columns)
df[['CurrentHeight','CurrentWeight','WeightOneYearAgo','Duration_ModerateActivity_PerSession','Frequency_ModerateActivity','age','SittingTime_TypicalDay','WeekdaySleepHours']]=imputed_df
imputer = KNNImputer(n_neighbors=1)
imputed_data = imputer.fit_transform(df)
df = pd.DataFrame(imputed_data, columns=df.columns)

df['bmi']=(df['CurrentWeight']/(df['CurrentHeight']**2))*703
df['weight_diff']=df['CurrentWeight']-df['WeightOneYearAgo']
df['activity_time']=df['Duration_ModerateActivity_PerSession']*df['Frequency_ModerateActivity']
df['EverTold_Diabetes']=df['EverTold_Diabetes'].astype(int)

category_cols=['race','GeneralHealth_Status','WorkExperience_LastWeek','SmokedAtLeast100CigarettesInLife']
df1 = pd.get_dummies(df, columns=category_cols)

X = df1.drop(['EverTold_Diabetes', 'sequence_no','CurrentHeight','CurrentWeight','WeightOneYearAgo','Duration_ModerateActivity_PerSession','Frequency_ModerateActivity'], axis=1) 
y = df1['EverTold_Diabetes']
X_np = X.to_numpy()
y_np = y.to_numpy()
num_col_reduced=['age','sample_weight','sample_weight2','SittingTime_TypicalDay','WeekdaySleepHours','AlcoholConsumptionFrequency_12Months','weight_diff','activity_time']
numeric_column_indices = [X.columns.get_loc(col) for col in num_col_reduced]                     

parser = argparse.ArgumentParser(description="Train a model with a specified sampler")
parser.add_argument("--model", type=str, required=True, help="Model name: RandomForest, LogisticRegression, SVM")
parser.add_argument("--sampler", type=str, required=True, help="Sampler: None, SMOTE, ADASYN, TomekLinks, SMOTETomek")
args = parser.parse_args()


if args.sampler == "SMOTE":
    sampler = SMOTE(random_state=42)
elif args.sampler == "ADASYN":
    sampler = ADASYN(random_state=42)
elif args.sampler == "TomekLinks":
    sampler = TomekLinks()
elif args.sampler == "SMOTETomek":
    sampler = SMOTETomek(random_state=42)
else:
    sampler = None


# Select model
if args.model == "RandomForest":
    model = RandomForestClassifier(bootstrap= True, max_features= 'sqrt', min_samples_leaf= 1, min_samples_split= 10, n_estimators= 100,random_state=42)
elif args.model == "LogisticRegression":
    model = LogisticRegression(penalty='l1', solver='liblinear', random_state=42, max_iter=500, class_weight='balanced')
elif args.model == "SVM-rbf":
    model = SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=42)
elif args.model == "SVM-linear":
    model = SVC(kernel='linear', probability=True, class_weight='balanced', random_state=42)
elif args.model == "XGBoost":
    model = xgb.XGBClassifier(eval_metric='logloss', random_state=42)
else:
    raise ValueError("Invalid model name. Choose from RandomForest, LogisticRegression, SVM.")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
preprocessor = ColumnTransformer(
    transformers=[('scaler', StandardScaler(), numeric_column_indices)],
    remainder='passthrough' 
)

auc_scores = []
accuracy_scores = []

for train_idx, valid_idx in skf.split(X_np, y_np):
    X_train, X_valid = X[train_idx], X[valid_idx]
    y_train, y_valid = y[train_idx], y[valid_idx]

    X_train = preprocessor.fit_transform(X_train)
    X_valid = preprocessor.transform(X_valid)

    if sampler:
        X_train, y_train = sampler.fit_resample(X_train, y_train)

    model.fit(X_train, y_train)

    y_pred_proba = model.predict_proba(X_valid)
    y_pred = (y_pred_proba[:, 1] >= 0.5).astype(int)

    auc_roc = roc_auc_score(y_valid, y_pred_proba[:, 1])
    accuracy = accuracy_score(y_valid, y_pred)

    auc_scores.append(auc_roc)
    accuracy_scores.append(accuracy)

avg_auc = np.mean(auc_scores)
avg_accuracy = np.mean(accuracy_scores)

print(f"Model: {args.model}, Sampler: {args.sampler}")
print(f"Average AUC-ROC: {avg_auc:.4f}, Average Accuracy: {avg_accuracy:.4f}")

model.fit(X_train, y_train)
