import json
import requests
import pandas as pd
import numpy as np 

storm_url = "https://www.hko.gov.hk/wservice/tsheet/pms/ssdb_storm.js?_=1551235660632"

html = requests.get(storm_url)
d = json.loads(html.content)

level_1 = ['ENG', 'CHN', 'YEAR', 'MONTH', 'TYPE']

#df_list = [] # list to store rows of basic info
REC_col = [] # list to store rows of data info

for i, values in d.items(): #iteriate through the first key, i.e., the typhoon name
    dt = {} # basic info per row
    for j in level_1: #get data
        #print(d[str(i)][j])
        dt[j] = d[str(i)][j] #construct dictionary of data
    
    #df_list.append(dt) #append the dictionary

    ####### get stations data #####
    d_REC = d[str(i)]['REC'] #station data stored under REC key
    for REC, values in d_REC.items(): # iteriate through the keys of REC
        REC_dict = {} #dirction to store data
        REC_dict["Stations"] = REC
        for data, v in values.items(): #iterate through the keys of REC station data
            REC_dict[data] = v

        for j in level_1: #add back the basic information
            REC_dict[j] = d[str(i)][j]

        REC_col.append(REC_dict)

        

#print(df_list)

station = pd.DataFrame(REC_col)
#station.to_csv("stormSurgeData.csv")
station[['YEAR','MONTH','Stations']] = station[['YEAR','MONTH','Stations']].apply(pd.to_numeric, errors = 'ignore')

stations_name = {
1:"Quarry Bay", 
2:"Shek Pik", 
3:"Tai Miu Wan", 
4:"Tai Po Kau", 
5: "Tsim Bei Tsui", 
6:"Waglan Island", 
7:"North Point", 
8:"Chi Ma Wan", 
9:"Lok On Pai", 
10:"Tai O", 
11:"Ko Lau Wan"
 }

station = station.replace({'Stations': stations_name})

station.to_csv("stormSurgeData.csv")

pivot = pd.pivot_table(station, values=['SEA', 'SEA_TIME', 'SURGE', 'SURGE_TIME'], index = ['YEAR','MONTH','CHN', 'ENG','TYPE']
, columns=['Stations'], aggfunc=np.sum)

pivot.columns = pivot.columns.swaplevel(1, 0)
pivot.to_csv("stormSurgeData_summary.csv")

