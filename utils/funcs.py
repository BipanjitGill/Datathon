import pandas as pd 
import matplotlib.pyplot as plt

def get_variable_names(path='E:/sem5/datathon/variables.csv'):
    '''Returns a dictionary of variables and their new names'''
        
    with open(path, mode='r', encoding='utf-8', errors='replace') as f:
        df_vars = pd.read_csv(f)
    
    variables_mapping=dict(zip(df_vars['Variable Name'], df_vars['Renamed_variables']))

    return variables_mapping

def rename_columns(df, variables_mapping):
    '''Returns a dataframe with renamed columns'''
    df.rename(columns=variables_mapping, inplace=True)
    return df

def processed_diabetes_data(path='E:/sem5/datathon/raw_datasets/diabetes.XPT'):
    df=pd.read_sas(path, format='xport')
    mapping=get_variable_names()
    df=rename_columns(df, mapping)
    df = df[df['EverTold_Diabetes'].isin([1.0, 2.0])]
    return df

def single_histogram(array,x_label,y_label,title,bins=20,density=True,to_save=False,loc="E:/sem5/datathon/images/"):
    plt.figure(figsize=(10, 6))  
    plt.hist(array, bins=bins, density=density, alpha=0.5)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    if to_save:
        plt.savefig(loc+title+".png")

def double_histogram(array1,array2,x1_label,x2_label,y_label,title,bins=20,density=True,to_save=False,loc="E:/sem5/datathon/images/"):
    plt.figure(figsize=(10, 6))  
    plt.hist(array1, bins=bins, density=density, alpha=0.5, label=x1_label, color='blue')
    plt.hist(array2, bins=bins, density=density, alpha=0.5, label=x2_label, color='red')
    plt.title(title)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    if to_save:
        plt.savefig(loc+title+".png")