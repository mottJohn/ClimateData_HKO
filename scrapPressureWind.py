import pandas as pd 
import ast
import requests

import json
from pprint import pprint

with open('aws.json') as f:
    data = json.load(f)

#pprint(data['aws'])

"""
for lst in data['aws']:
    print(lst['startYear'])
"""

errors = []
for lst in data['aws']:
    station = lst['code']
    result = pd.DataFrame()

    for year in list(range(lst['startYear'], lst['endYear']+1)):
        tide_url = "http://www.hko.gov.hk/cis/aws/dailyExtract/dailyExtract_{}_{}.xml".format(station, year)
        print(tide_url)
        
        html = requests.get(tide_url)
        
        try:
            d = json.loads(html.content)
        

            for month in list(range(lst['startMonth']-1,lst['endMonth'])):
                df = pd.DataFrame(d['stn']['data'][month])
                try:
                    df_2 = pd.DataFrame(df.dayData.values.tolist(), columns=[ "Day", "Mean Pressure (hPa)", "Air Temperature Absolute Daily Max (deg. C)","Air Temperature Mean (deg.C)", "Air Temperature Absolute Daily  Min (deg. C)",
                    "Mean Dew Point (deg. C)", "Mean Relative Humidity (%)","Mean Relative Humidity (%)", "Total Rainfall (mm)",
                    "Prevailing Wind Direction (degrees)", "Mean Wind Speed (km/h)"])
                except:
                    df_2 = pd.DataFrame(df.dayData.values.tolist(), columns=[ "Day", "Mean Pressure (hPa)", "Air Temperature Absolute Daily Max (deg. C)","Air Temperature Mean (deg.C)", "Air Temperature Absolute Daily  Min (deg. C)",
                    "Mean Dew Point (deg. C)","Mean Relative Humidity (%)", "Total Rainfall (mm)",
                    "Prevailing Wind Direction (degrees)", "Mean Wind Speed (km/h)"])
                #df_2 = pd.DataFrame(df.dayData.values.tolist())
                #print(df_2)
                df_2['Year'] = year
                df_2['Month'] = month + 1
        
        #df_2.to_csv('test.csv')
        #print(df_2)

                try:
                    result = pd.concat([result, df_2])
                except:
                    result = df_2
        except:
            errors.append(tide_url)

        
    cols = result.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    result = result[cols]

    fileName = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\HKO Data for Climate Change\MetData" + "/" "dailyExtractMetData_{}.csv".format(station)
    if result.empty:
        pass
    else:
        result.to_csv(fileName, index= False)
    #print(result)

er = pd.DataFrame(errors)
er.to_csv('errors_met.csv')
