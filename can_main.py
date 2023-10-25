import csv
import pandas as pd
import numpy as np
import seaborn as sns

from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt

import re
import math

weather_melbourne = pd.read_csv('dataset/weather_melbourne.csv', parse_dates=['Date'])
#weather_sydney = pd.read_csv('dataset/weather_sydney.csv', parse_dates=['Date'])
#weather_brisbane = pd.read_csv('dataset/weather_brisbane.csv', parse_dates=['Date'])
#weather_adelaide = pd.read_csv('dataset/weather_adelaide.csv', parse_dates=['Date'])

price_demand_data = pd.read_csv(
    'dataset/price_demand_data.csv', 
    index_col=0, 
    parse_dates=['SETTLEMENTDATE']
)

# Function to rename each columns to something more typeable/readable.
def rename_columns_weather(pandas_dataframe):
    for col in pandas_dataframe:
        # Removing spaces and unit types  (e.g., min_temp (Celcius))
        new_header = re.sub(r'\(.+\)', '', col).lower()
        new_header = re.sub(r'\s+', ' ', new_header)
        new_header = re.sub(r' ', '_', new_header)
        new_header = re.sub(r'_$', '', new_header)
        # Creating abbreviations
        new_header = re.sub(r'maximum', 'max', new_header)
        new_header = re.sub(r'minimum', 'min', new_header)
        new_header = re.sub(r'temperature', 'temp', new_header)
        new_header = re.sub(r'direction', 'dir', new_header)
        new_header = re.sub(r'pressure', 'pres', new_header)
        new_header = re.sub(r'humidity', 'hume', new_header)
        new_header = re.sub(r'_of_', '_', new_header)

        pandas_dataframe.rename(columns={col: new_header}, inplace=True)
    return pandas_dataframe

# Apply to all weather city data
for city in [weather_melbourne]: # , weather_sydney, weather_brisbane, weather_adelaide
    rename_columns_weather(city)

price_demand_data.rename(columns={
    'REGION': 'region',
    'SETTLEMENTDATE': 'settlement_date',
    'TOTALDEMAND': 'total_demand',
    'PRICESURGE': 'price_surge'
}, inplace=True)

#nsw_pdd = price_demand_data.loc[price_demand_data.index == 'NSW1']
#qld_pdd = price_demand_data.loc[price_demand_data.index == 'QLD1']
#sa_pdd = price_demand_data.loc[price_demand_data.index == 'SA1']
vic_pdd = price_demand_data.loc[price_demand_data.index == 'VIC1']



def temp_v_demand(demand, city):

    city_9temp = city.loc[:,['date','9am_temp']]
    city_3temp = city.loc[:,['date','3pm_temp']]

    demand_9 = demand.loc[:, ['settlement_date', 'total_demand']]
    demand_9 = demand_9.set_index('settlement_date')
    demand_9 = demand_9.at_time('9:00')
    demand_9=  demand_9.reset_index()

    demand_3 = demand.loc[:, ['settlement_date', 'total_demand']]
    demand_3 = demand_3.set_index('settlement_date')
    demand_3 = demand_3.at_time('15:00')
    demand_3=  demand_3.reset_index()

    temp_demand_9 = pd.concat([city_9temp, demand_9], ignore_index=True)
    temp_demand_9 = city_9temp.join(demand_9['total_demand'])

    temp_demand_3 = pd.concat([city_3temp, demand_3], ignore_index=True)
    temp_demand_3 = city_3temp.join(demand_3['total_demand'])

    return {9 : temp_demand_9, 3 : temp_demand_3}

def variable_v_demand(demand, city, variable):

    city_var = city.loc[:,['date', str(variable)]]

    city_var = city_var.set_index('date')
    city_var = city_var.reset_index()
    demand = demand.reset_index()
    demand.rename(columns = {'settlement_date' : 'date'}, inplace=True)


    return demand.join(city_var[str(variable)])
    #var_demand = city_9temp.join(demand_9['total_demand'])



def avg_demand_perday(state):
    return state.groupby(pd.PeriodIndex(state['settlement_date'], freq="D"))['total_demand'].mean()
    

vic_day_avg = avg_demand_perday(vic_pdd)
#sa_day_avg = avg_demand_perday(sa_pdd)
#qld_day_avg = avg_demand_perday(qld_pdd)
#nsw_day_avg = avg_demand_perday(nsw_pdd)

#print(variable_v_demand(vic_day_avg, weather_melbourne, 'rainfall'))

for i in weather_melbourne:

    if i != 'date' and (type(weather_melbourne[i][1]) != str):
        table = variable_v_demand(vic_day_avg, weather_melbourne, str(i))
        grph = table.plot(x= str(i), y='total_demand', kind = 'scatter')
        grph.figure.savefig('{}.png'.format(str(i)))

































#test = temp_v_demand(vic_pdd, weather_melbourne, )
#print(test)

#grph = test[3].plot(x='3pm_temp', y='total_demand', kind = 'scatter')
    




#melb_9temp = weather_melbourne.loc[:,['date','9am_temp']]
#melb_3temp = weather_melbourne.loc[:,['date','3pm_temp']]

#vic_9_demand = vic_pdd.loc[:, ['settlement_date', 'total_demand']]
#vic_9_demand = vic_9_demand.set_index('settlement_date')
#vic_9_demand = vic_9_demand.at_time('9:00')
#vic_9_demand=  vic_9_demand.reset_index()

#vic_3_demand = vic_pdd.loc[:, ['settlement_date', 'total_demand']]
#vic_3_demand = vic_3_demand.set_index('settlement_date')
#vic_3_demand = vic_3_demand.at_time('15:00')


#melb_9temp_demand = pd.concat([melb_9temp, vic_9_demand], ignore_index=True)
#melb_9temp_demand = melb_9temp.join(vic_9_demand['total_demand'])



#grph = melb_9temp_demand.plot(x='9am_temp', y='total_demand', kind = 'scatter')

#grph.figure.savefig('test.png')



