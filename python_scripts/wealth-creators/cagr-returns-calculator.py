
import time
import random 
import pandas as pd
import numpy as np 
import csv
import datetime
import mysql.connector

#cnx = mysql.connector.connect(host="localhost", database='nse_stats', user='boui', password= 'boui')
cnx = mysql.connector.connect(host="localhost", database='nse_stats', user='root', password= '123456')


invalid_stocks_file = "../common/Invalid.csv"
bse_all_stocks_file = "../common/BSE_ALL.csv"

manually_confirmed_invalid_file = "../common/manually-confirmed-invalid.csv"

chart_ink_file = 'chart_ink_stocks.csv'

# actual code
chart_ink_filtered_stocks_1 = {'HDFCBANK', 'ICICIBANK'}

invalid_data = pd.read_csv(invalid_stocks_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
bse_all = pd.read_csv(bse_all_stocks_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
manually_invalid_data = pd.read_csv(manually_confirmed_invalid_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)

# print('\invalid dataframe :\n', invalid_data)

invalid_stocks_set = set(invalid_data['Security Id'].tolist())
invalid_stocks_set = invalid_stocks_set.union(invalid_data['Security Code'].tolist())
invalid_stocks_set = invalid_stocks_set.union(invalid_data['ISIN No'].tolist())
invalid_stocks_set = invalid_stocks_set.union(manually_invalid_data['Security Code'].tolist())

#non-shariah stocks
#print(invalid_stocks_set)


def write_ouput(returns_list, csv_file_name):
        


    csv_header = ['ISIN-CODE', 'NSE-CODE', 'buy-date', 'buy-price', 'sell-date', 'sell-price',  'buy-share-count', 'returns-share-count', 'invested', 'cumulative-returns', 'n-return-times' , 'CAGR', "corporate-action-count"]
    csv_file = open(csv_file_name, 'w', newline='')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(i for i in csv_header)

    for item in returns_list:        
        writer.writerow(item)
    csv_file.close()

def cagr_percentage (start_value, end_value, num_periods):
    cagr = (end_value / start_value) ** (1 / num_periods ) - 1
    #converting into rounded percentage
    return int(cagr * 100)

cursor = cnx.cursor()
#stock_price_query = "SELECT trade_date, isin_code, nse_code, close_price FROM stock_prices WHERE nse_code in ('HCLTECH', 'ICICIBANK', 'INFY', 'VOLTAS')  ORDER BY trade_date"
stock_price_query = "SELECT trade_date, isin_code, nse_code, close_price FROM stock_prices  ORDER BY trade_date"
output_dict = {}
invest_amount = 50000

cursor.execute(stock_price_query)
for (stock_price_row) in cursor :
    
    if stock_price_row[1] in invalid_stocks_set:
        #skipping invalid stocks
        continue
    
    my_value = output_dict.get(stock_price_row[1])
    
    if my_value is None:
        #date, nse-code, close-price, shares-count
        output_dict[stock_price_row[1]] = [[stock_price_row[0], stock_price_row[2], stock_price_row[3], int( invest_amount/ stock_price_row[3]) ]] 
    else :
        initial_shares_bought = my_value[0][3];
        #date, nse-code, close-price, shares-count, corporate-action-count
        my_value.append([stock_price_row[0], stock_price_row[2], stock_price_row[3], initial_shares_bought, 0])
        
#cursor.close()

csv_rows = []    

corporate_aciton_query = "SELECT action, event_date, ratio_prefix , ratio_suffix FROM stock_corporate_actions WHERE isin_code = "
order_by = " ORDER BY event_date"

delisted_stocks = {}
for key, value in output_dict.items():
    
    if len(value) == 1:
        #stock got delitsted, so skipping
        delisted_stocks[key] = value
        continue
        
    invest_record = value[0]
    
    
    returns_record = value[1]
    nse_code = invest_record[1]
    
    query_1 = corporate_aciton_query + "'" + key + "'" + order_by
    # print(query_1)
    cursor.execute(query_1)
    for (event) in cursor :
        retruns_share_count = returns_record[3]        
        
        if event[0] == "BONUS" :
            additional_shares = int( retruns_share_count * (event[2]/event[3]))
            returns_record[3] = retruns_share_count +  additional_shares
        elif event[0] == "SPLIT" :
            splitted_shares = int( retruns_share_count * (event[2]/event[3]))
            returns_record[3] = splitted_shares
        else :
            #skpping other actions
            continue
        
        
        returns_record[4] = returns_record[4] + 1
            
    
    cumulative_returns = returns_record[2] * returns_record[3]
    n_times_return = int(cumulative_returns / invest_amount)
    cagr = cagr_percentage(invest_amount, cumulative_returns, 12)
    #ISIN-CODE, NSE-CODE,buy-date, buy-price, sell-date, sell-price,  buy-share-count, returns-share-count, invested, cumulative-returns, n-return-times , cagr, corporate-action-count
    csv_rows.append([key, invest_record[1], invest_record[0], invest_record[2], returns_record[0], returns_record[2], invest_record[3], returns_record[3], invest_amount,  cumulative_returns, n_times_return, cagr ,returns_record[4] ])
    
    
#print(output_dict)
#print(csv_rows)

write_ouput(csv_rows, "2009-2020-lumpsump-returns-11.csv")
print("wealth-creation-file-stats is ready")
cursor.close()    
cnx.close()