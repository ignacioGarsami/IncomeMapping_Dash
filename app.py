import utils
import os


data = utils.data_handler()
os.remove("kaggle_income.csv.zip")

print(data.head())