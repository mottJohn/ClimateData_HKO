import pandas as pd 
import ast
import requests

import json


tideGaugeStations = ['TBT','QUB','SHP','TMW','TPK','WAG']

for station in tideGaugeStations:
    result = pd.DataFrame()

    for year in list(range(1954, 2019)):
        tide_url = "http://www.hko.gov.hk/cis/aws/tide/daily_{}_TIDE_{}.xml".format(station, year)

        #print(tide_url)
        html = requests.get(tide_url)
        try:
            d = json.loads(html.content)
        

            for month in list(range(0,12)):
                df = pd.DataFrame(d['tide']['data'][month])
                df_2 = pd.DataFrame(df.dayData.values.tolist(), columns=['Day', 'Mean Sea Level','Higher High Water Height', 
            'Higher High Water Time', 'Lower High Water Height', 'Lower High Water Time', 'Higher Low Water Height', 'Higher Low Water Time', 'Lower Low Water Height', 'Lower Low Water Time'])

                df_2['Year'] = year
                df_2['Month'] = month + 1
       
        #df_2.to_csv('test.csv')
        #print(df_2)

                try:
                    result = pd.concat([result, df_2])
                except:
                    result = df_2

        except:
            pass
    cols = result.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    result = result[cols]

    fileName = "dailyObservedSeaLevels_{}.csv".format(station)
    result.to_csv(fileName, index= False)
    #print(result)