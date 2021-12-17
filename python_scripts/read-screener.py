import requests 
from bs4 import BeautifulSoup
import time
import random 
import pandas as pd
import numpy as np 
import csv
import datetime

shariah_stocks_2_last_page = 10
shariah_stocks_3_last_page = 10


shariah_stocks_1_last_page = 74 

shariah_stocks_2_last_page = 48

shariah_stocks_3_last_page = 78


invalid_stocks_file = "invalid.csv"
bse_all_stocks_file = "BSE_ALL.csv"

# actual code
# shariah_stocks_1 = {'TCS', 'HDFCBANK', 'ICICIBANK', '20MICRONS', '3PLAND', '517356', '520123', '524091', '530043', '531161', '531525', '538952', '539300', '539562', '539661', '540135', '540615', 'AAKASH', 'AARON', 'AARTIDRUGS', 'AARTIIND', 'AARVI', 'ABB', 'ABINFRA', 'ABMINTLTD', 'ACC', 'ACCELYA', 'POWERINDIA', 'TCS'}
shariah_stocks_1 = {'TCS', 'HDFCBANK', 'ICICIBANK'}
shariah_stocks_2 = {'TCS', 'HDFCBANK', 'ICICIBANK'}
shariah_stocks_3 = {'TCS', 'HDFCBANK', 'ICICIBANK'}  
shariah_stocks_all = {'TCS', 'HDFCBANK', 'ICICIBANK'}

shariat_url_1 = "https://www.screener.in/screens/301123/MasnoonShariahCompliant1/?sort=name&order=asc&page="

shariat_url_2 = "https://www.screener.in/screens/301131/MasnoonShariahCompliant2/?sort=name&order=asc&page="

shariat_url_3 = "https://www.screener.in/screens/301613/MasnoonShariahCompliant3/?sort=name&order=asc&page="

invalid_data = pd.read_csv(invalid_stocks_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
bse_all = pd.read_csv(bse_all_stocks_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)

# print('\invalid dataframe :\n', invalid_data)

invalid_stocks_set = set(invalid_data['Security Id'].tolist())
invalid_stocks_set =  invalid_stocks_set.union(invalid_data['Security Code'].tolist())


def get_screener_stocks(screener_url, stocks_collection):
    print("url: " + screener_url)
    resp = requests.get(screener_url) 
    # http_respone 200 means OK status 
    if resp.status_code == 200: 
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for a_tag in soup.find_all('a', href=True):
            href_url = a_tag['href'] 
            if '/company/' in href_url:
                spiltted = href_url.split("/")                
                stocks_collection.add(spiltted[2])
                shariah_stocks_all.add(spiltted[2])
     
    else:
        print ("error in fetching url: " + screener_url)


def prepare_stocks(screener_url, last_page, stocks_list):
    for i in range(1, last_page):
        fetch_url = screener_url + str(i)        
        time.sleep(1.1 + random.randint(0, 999) / 1000)
        get_screener_stocks(fetch_url, stocks_list)


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

# prepare_stocks(shariat_url_1, shariah_stocks_1_last_page, shariah_stocks_1)
# filter_process_stock_data(shariah_stocks_1, 'shariah_compliant_1.csv')


print("Finished Shariah 1")

prepare_stocks(shariat_url_2, shariah_stocks_2_last_page, shariah_stocks_2)
filter_process_stock_data(shariah_stocks_2, 'shariah_compliant_2.csv')

print("Finished Shariah 2")

prepare_stocks(shariat_url_3, shariah_stocks_3_last_page, shariah_stocks_3)
filter_process_stock_data(shariah_stocks_3, 'shariah_compliant_3.csv')

print("Finished Shariah 3")

filter_process_stock_data(shariah_stocks_all, 'shariah_compliant_all.csv')
print("Finished Shariah ALL")

