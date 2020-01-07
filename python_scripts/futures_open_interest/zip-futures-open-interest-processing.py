import sys
import requests
import pandas as pd 
import numpy as np
import mysql.connector

from zipfile import ZipFile 
from datetime import datetime
from dateutil.relativedelta import relativedelta

"""
#Bhavcopy file (csv)
url = 'https://www.nseindia.com/content/historical/DERIVATIVES/2019/DEC/fo31DEC2019bhav.csv.zip'
response = requests.get(url)
 
with open('raw-data.csv', 'wb') as file_write:
    file_write.write(response.content)


"""

def extract_csv_file(input_zip_file):
    with ZipFile(input_zip_file, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
      
         # Iterate over the file names
        for fileName in listOfFileNames:
           # Check filename endswith csv
           if fileName.endswith('.csv'):
               print('Extracted csv file: ' + fileName)
               
               csv_file_name = zipObj.extract(fileName)
               return csv_file_name             
               
           else:
               print('Wrong zip: ' + input_zip_file)
               sys.exit(1) 
    

input_zip_file = sys.argv[1]

input_file = extract_csv_file(input_zip_file)


# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
complete_data =  pd.read_csv(input_file, sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)


futures_stock = complete_data.drop(complete_data[complete_data["INSTRUMENT"] != 'FUTSTK'].index)
#futures_stock.drop(futures_stock[futures_stock["CLOSE"] < 90].index, inplace=True)

my_symbols = {'DUMMY_SET_VALUE'}

#cnx = mysql.connector.connect(host="localhost", database='nse_stats', user='root', password= '123456')
cnx = mysql.connector.connect(host="localhost", database='nse_stats', user='root', password= '123456')

cursor = cnx.cursor()
query = 'SELECT symbol FROM stocks WHERE is_fno = 1 '

cursor.execute(query)
for (my_symbol) in cursor :
    my_symbols.add(my_symbol[0])

cursor.close()

my_futures_stock = futures_stock[futures_stock['SYMBOL'].isin(my_symbols)]
print("my_futures_stock size : " )
print(my_futures_stock.shape)

print('-------------------------------------\n')

#getting date from first-row, last-column
file_date = my_futures_stock.iat[1,14]

print("processing oi for date " + file_date)
formatted_date = pd.to_datetime(file_date).strftime('%Y-%m-%d')







grouped = my_futures_stock.groupby('SYMBOL')



#DELETE  EXISTING FUTURE OIs OF Processing file

cursor = cnx.cursor()
delete_query = 'DELETE FROM future_oi_consolidated WHERE date = "' + formatted_date +'"'
print('Consolidated OI Delete query: ' + delete_query)
cursor.execute(delete_query)
cnx.commit()
cursor.close()

cursor = cnx.cursor()
delete_query = 'DELETE FROM future_series_oi WHERE date = "' + formatted_date +'"'
print('Series OI Delete query: ' + delete_query + "\n")
cursor.execute(delete_query)
cnx.commit()
cursor.close()

print('-----------------------------\n\n')

#ADDING FUTURE OIs OF Processing file 
current_time = pd.to_datetime('now').isoformat()

cursor = cnx.cursor()

insert_query = "INSERT INTO future_oi_consolidated(date, symbol, open_interest, open_interest_change, contracts, created_at) VALUES (%s, %s, %s, %s, %s, %s) "




my_row_values = []



for grouped_item, group_iter in grouped:
    
    #print(group['OPEN_INT'].agg(np.sum))
    my_row_values.append((formatted_date, grouped_item, str(group_iter['OPEN_INT'].agg(np.sum)), str(group_iter['CHG_IN_OI'].agg(np.sum)), str(group_iter['CONTRACTS'].agg(np.sum)), current_time))
    
    
cursor.executemany(insert_query, my_row_values)


print("For Consolidated OI successfully inserted " + str(len(my_row_values)) + " rows.")

cnx.commit()
cursor.close()

print('-------------------------------------\n')


unique_expries = my_futures_stock['EXPIRY_DT'].unique()

current_date = pd.to_datetime(file_date)
current_month = current_date.month

current_month_series_exists = False


#special case only 2 handle, contracts of 28-31 of any month, whose contracts
# might have expired due to last thursday varies

for item in unique_expries :
    print("Unique Series: " + item)
    if current_month == pd.to_datetime(item).month :
        current_month_series_exists = True
        break
        
    
if current_month_series_exists :
    print("Current Series Exists \n")
    next_month = (current_date + relativedelta(months=+1)).month
    next_2_next_month = (current_date + relativedelta(months=+2)).month
else :
    print("Current Series Not Exists \n")
    current_month = (current_date + relativedelta(months=+1)).month
    next_month = (current_date + relativedelta(months=+2)).month
    next_2_next_month = (current_date + relativedelta(months=+3)).month


print("current_month \t\t" + str(current_month))        
print("next_month \t\t" + str(next_month))    
print("next_2_next_month \t" + str(next_2_next_month))    
    

cursor = cnx.cursor()
series_insert_query = "INSERT INTO future_series_oi (date, symbol, series, raw_series, open, high, low, close,  open_interest, open_interest_change, contracts, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) "
my_row_values = []

for index, row in my_futures_stock.iterrows():
    
    
    row_date = pd.to_datetime(row['EXPIRY_DT'])
    
    series_value = 'current_month'
    if row_date.month == next_month:
        series_value = 'next_month'
    elif row_date.month == next_2_next_month :
        series_value = 'next_2_next_month'
        
    my_row_values.append((formatted_date, row['SYMBOL'], series_value, str(row['EXPIRY_DT']), str(row['OPEN']),  str(row['HIGH']),  str(row['LOW']),  str(row['CLOSE']),  str(row['OPEN_INT']), str(row['CHG_IN_OI']), str(row['CONTRACTS']), current_time))
    
    
print(my_row_values[1])    
cursor.executemany(series_insert_query, my_row_values)
print(" For Series OI successfully inserted " + str(len(my_row_values)) + " rows.")    

cnx.commit()
cursor.close()
    
    


cnx.close()



"""
print(complete_data.dtypes)
print(complete_data.columns)
print(complete_data.head())
print(complete_data.shape)

INSTRUMENT     object
SYMBOL         object
EXPIRY_DT      object
STRIKE_PR     float64
OPTION_TYP     object
OPEN          float64
HIGH          float64
LOW           float64
CLOSE         float64
SETTLE_PR     float64
CONTRACTS       int64
VAL_INLAKH    float64
OPEN_INT        int64
CHG_IN_OI       int64
TIMESTAMP      object
(31749, 15)

"""
