import requests 
from bs4 import BeautifulSoup
import time
import random 
import pandas as pd
import numpy as np 
import csv
import datetime

invalid_stocks_file = "invalid.csv"
bse_all_stocks_file = "BSE_ALL.csv"

manually_confirmed_invalid_file = "manually-confirmed-invalid.csv"

chart_ink_file = 'chart_ink_stocks.csv'

# actual code
chart_ink_filtered_stocks_1 = {'HDFCBANK', 'ICICIBANK'}

invalid_data = pd.read_csv(invalid_stocks_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
bse_all = pd.read_csv(bse_all_stocks_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
manually_invalid_data = pd.read_csv(manually_confirmed_invalid_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)

# print('\invalid dataframe :\n', invalid_data)

invalid_stocks_set = set(invalid_data['Security Id'].tolist())
invalid_stocks_set = invalid_stocks_set.union(invalid_data['Security Code'].tolist())
invalid_stocks_set = invalid_stocks_set.union(manually_invalid_data['Security Code'].tolist())

print(invalid_stocks_set)


def filter_process_stock_data(stocks_list, csv_file_name):
        
    # removing invalid stocks
    stocks_list = set(set(stocks_list).difference(invalid_stocks_set))    
    stocks_list = sorted(stocks_list)

    csv_header = ["StockId", "StockName", "Company", "Industry"]
    csv_file = open(csv_file_name, 'w', newline='')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(i for i in csv_header)

    for item in stocks_list:
        row = [item]
        if item.isnumeric():
            result_df = bse_all.loc[(bse_all['Security Id'] == item) | (bse_all['Security Code'] == int(item))]        
        else:
            result_df = bse_all.loc[bse_all['Security Id'] == item]
        
        for df_row in result_df.itertuples():
           row.extend([df_row[3], df_row[4], df_row[9]])       
           
        if len(row) == 1:
            row.append(item)  
        writer.writerow(row)
    csv_file.close()


f = open(chart_ink_file, "r")
for x in f:
  chart_ink_filtered_stocks_1.add(x.strip())
f.close()
print(sorted(chart_ink_filtered_stocks_1))
print ("Loaded chart-ink stocks size: %d", len(chart_ink_filtered_stocks_1))

filter_process_stock_data(chart_ink_filtered_stocks_1, "filtered_" + chart_ink_file)

print("Finished Shariah ALL")

