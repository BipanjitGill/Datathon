import pandas as pd 

def get_variable_names(path='variables.csv'):
    '''Returns a dictionary of variables and their new names'''
        
    with open(path, mode='r', encoding='utf-8', errors='replace') as f:
        df_vars = pd.read_csv(f)
    
    variables_mapping=dict(zip(df_vars['Variable Name'], df_vars['Renamed_variables']))

    return variables_mapping

def rename_columns(df, variables_mapping):
    '''Returns a dataframe with renamed columns'''
    df.rename(columns=variables_mapping, inplace=True)
    return df

def processed_diabetes_data(path='raw_datasets/diabetes.XPT'):
    df=pd.read_sas(path, format='xport')
    mapping=get_variable_names()
    df=rename_columns(df, mapping)
    df = df[df['EverTold_Diabetes'].isin([1.0, 2.0])]
    return df
     