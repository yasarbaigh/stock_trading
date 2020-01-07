import sys
import requests
import pandas as pd 
import numpy as np
import datetime
import mysql.connector

from datetime import datetime


input_file = sys.argv[1]

"""
#Bhavcopy file (csv)
# https://www.nseindia.com/products/content/equities/equities/eq_security.htm
url = 'https://www.nseindia.com/products/content/sec_bhavdata_full.csv'
response = requests.get(url)
 
with open('raw-data.csv', 'wb') as file_write:
    file_write.write(response.content)


"""


# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
complete_data =  pd.read_csv(input_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)


equity_series_stock = complete_data.drop(complete_data[complete_data["SERIES"] != 'EQ'].index)
#equity_series_stock.drop(equity_series_stock[equity_series_stock["CLOSE"] < 90].index, inplace=True)

my_symbols = {'DUMMY_SET_VALUE'}

#cnx = mysql.connector.connect(host="localhost", database='nse_stats', user='boui', password= 'boui')
cnx = mysql.connector.connect(host="localhost", database='nse_stats', user='root', password= '123456')

cursor = cnx.cursor()
query = 'SELECT symbol FROM stocks '

cursor.execute(query)
for (my_symbol) in cursor :
	my_symbols.add(my_symbol[0])

cursor.close()

my_equity_stocks = equity_series_stock[equity_series_stock['SYMBOL'].isin(my_symbols)]
print("my_equity_stocks size : " )
print(my_equity_stocks.shape)

#getting date from first-row, third-column
file_date = my_equity_stocks.iat[1,2]

print("processing delivery-quantity for date " + file_date)
formatted_date = pd.to_datetime(file_date).strftime('%Y-%m-%d')








#DELETE  EXISTING FUTURE OIs OF Processing file

cursor = cnx.cursor()
delete_query = 'DELETE FROM stock_delivery_quantity WHERE date = "' + formatted_date +'"'
print('delete query: ' + delete_query)
cursor.execute(delete_query)
cnx.commit()
cursor.close()



#ADDING FUTURE OIs OF Processing file 
current_time = pd.to_datetime('now').isoformat()

cursor = cnx.cursor()

insert_query = "INSERT INTO stock_delivery_quantity (date, symbol, prev_close, open, high, low, close, vwap, volume, delivery_quantity, delivery_percentage, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

my_row_values = []


for index, row in my_equity_stocks.iterrows(): 

	
	my_row_values.append((formatted_date, row['SYMBOL'], str(row['PREV_CLOSE']), str(row['OPEN_PRICE']), str(row['HIGH_PRICE']), str(row['LOW_PRICE']), str(row['CLOSE_PRICE']), str(row['AVG_PRICE']), str(row['TTL_TRD_QNTY']), str(row['DELIV_QTY']), str(row['DELIV_PER']),  current_time))
	
	
cursor.executemany(insert_query, my_row_values)


print("successfully inserted " + str(len(my_row_values)) + " rows.")

cnx.commit()
cursor.close()


cnx.close()




"""
print(complete_data.dtypes)
print(complete_data.columns)
print(complete_data.head())
print(complete_data.shape)

SYMBOL            object
SERIES            object
DATE1             object
PREV_CLOSE       float64
OPEN_PRICE       float64
HIGH_PRICE       float64
LOW_PRICE        float64
LAST_PRICE       float64
CLOSE_PRICE      float64
AVG_PRICE        float64
TTL_TRD_QNTY       int64
TURNOVER_LACS    float64
NO_OF_TRADES       int64
DELIV_QTY         object
DELIV_PER         object

(1946, 15)


"""