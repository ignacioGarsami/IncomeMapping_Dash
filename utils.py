from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import os

def data_handler():

    api = KaggleApi()
    api.authenticate()
    
    api.dataset_download_file('goldenoakresearch/us-household-income-stats-geo-locations', 'kaggle_income.csv')
    
    data = pd.read_csv('kaggle_income.csv.zip', encoding = 'cp1252')
    
    print('data downloaded')
    

    
    return(data)
    
