import sys
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)



import pandas as pd 
  
record = { 
  'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka', 'Priya', 'Shaurya' ], 
  'Age': [21, 19, 20, 18, 17, 21], 
  'Stream': ['Math', 'Commerce', 'Science', 'Math', 'Math', 'Science'], 
  'Percentage': [88, 92, 95, 70, 65, 78]} 
  
# create a dataframe 
dataframe = pd.DataFrame(record, columns = ['Name', 'Age', 'Stream', 'Percentage']) 
  
#print("Given Dataframe :\n", dataframe)  
  
# selecting rows based on condition 
rslt_df = dataframe.loc[(dataframe['Percentage'] == 92) | (dataframe['Stream'] == 'Commerce')] 
  
for i in rslt_df.itertuples():
    print(i[3])
#print('\nResult dataframe :\n', rslt_df) 