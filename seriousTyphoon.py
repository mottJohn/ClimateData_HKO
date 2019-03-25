import pandas as pd 
import matplotlib.pyplot as plt
import glob
import numpy as np

data = pd.read_csv("stormSurgeData.csv") #storm surge raw data
data_raw = data.copy()

data = data[data["SEA_TIME"] >= "2000"] # filter year after 2000
data_grouped = data.groupby(["YEAR", "ENG"]).mean() #many stations. take the average (year, eng is unique)
data_grouped = data_grouped.nlargest(6, "SURGE") #filter the largest 6

data = data[data["ENG"].isin(data_grouped.index.get_level_values(1)) & data["YEAR"].isin(data_grouped.index.get_level_values(0))]

data["SURGE_TIME"] = pd.to_datetime(data["SURGE_TIME"]) #convert to datetime
data["Date"] = (data["SURGE_TIME"].dt.year).astype(str) + '-' + (data["SURGE_TIME"].dt.month).astype(str) + '-' +(data["SURGE_TIME"].dt.day).astype(str) #concat to string for filter

#function get all files
def getFiles (path, type):
    allFiles = glob.glob(path + "/*.{}".format(type))
    
    return allFiles

tideData_path = r"C:\Users\CHA82870\Mott MacDonald\CLP Group Env Framework - Data\Data Analysis\tideData" #all tideData files

files = getFiles(tideData_path, "csv")

tideData = pd.DataFrame()
for f in files:
    temp = pd.read_csv(f)
    temp["Station"] = f[-7:-4]
    try:
        tideData = pd.concat([tideData, temp])
    except:
        tideData = temp 

tideData['Date'] = tideData["Year"].astype(str) + '-' + tideData["Month"].astype(str) + '-' + tideData["Day"].astype(str) #data column
tideData = tideData[tideData['Date'].isin(data['Date'])] #filter typhoon date

tideData['Higher High Water Time'] = tideData['Date'] + ' ' + tideData['Higher High Water Time'] #convert to datetime string
tideData['Higher Low Water Time'] = tideData['Date'] + ' ' + tideData['Higher Low Water Time']
tideData['Lower High Water Time'] = tideData['Date'] + ' ' + tideData['Lower High Water Time']
tideData['Lower Low Water Time'] = tideData['Date'] + ' ' + tideData['Lower Low Water Time']

tideData['Higher High Water Time'] = pd.to_datetime(tideData['Higher High Water Time'], errors = 'coerce') #convert to datetime
tideData['Higher Low Water Time'] = pd.to_datetime(tideData['Higher Low Water Time'], errors = 'coerce')
tideData['Lower High Water Time'] = pd.to_datetime(tideData['Lower High Water Time'], errors = 'coerce')
tideData['Lower Low Water Time'] = pd.to_datetime(tideData['Lower Low Water Time'], errors = 'coerce')

tideData = tideData.dropna() #drop nan

concat_tideData_1 = tideData[["Date", "Station", "Higher High Water Time", "Higher High Water Height"]] #4 cycle
concat_tideData_2 = tideData[["Date", "Station", "Higher Low Water Time", "Higher Low Water Height"]]
concat_tideData_3  = tideData[["Date", "Station", "Lower High Water Time", "Lower High Water Height"]]
concat_tideData_4 = tideData[["Date", "Station", "Lower Low Water Time", "Lower Low Water Height"]]

concat_tideData_1.columns = ["Date", "Station","DateTime", "Water Height"] #change the column name to be the same for concat
concat_tideData_2.columns = ["Date", "Station","DateTime", "Water Height"]
concat_tideData_3.columns = ["Date", "Station","DateTime", "Water Height"]
concat_tideData_4.columns = ["Date", "Station","DateTime", "Water Height"]

concat_tideData = pd.concat([concat_tideData_1, concat_tideData_2, concat_tideData_3, concat_tideData_4])

concat_tideData['Water Height'] = pd.to_numeric(concat_tideData['Water Height'], errors='coerce') #to numeric. some with ****, ---- with be nan
concat_tideData = concat_tideData.dropna() #drop nan
concat_tideData = concat_tideData.sort_values(by = 'DateTime', ascending = False)

concat_tideData = pd.merge(concat_tideData, data[["Date", "CHN", "ENG"]].drop_duplicates(), on = "Date") #get the name of typhoon
concat_tideData["Typhoon Date"] = concat_tideData["ENG"] + ' ' + concat_tideData["Date"] #some name is repeated. concat with date to get unique

for typhoon in concat_tideData["Typhoon Date"].unique(): #plot all stations data to one graph per typhoon
    fig, ax = plt.subplots()
    for key, grp in concat_tideData[concat_tideData["Typhoon Date"] == typhoon].groupby(["Station"]):
        ax = grp.plot(ax=ax, kind='line', x = "DateTime", y = "Water Height", label=key, title = typhoon)

    plt.savefig('{}.png'.format(typhoon))

with pd.ExcelWriter("seriousTyphoon.xlsx") as writer:
    data_raw.to_excel(writer, sheet_name = "Raw Storm Surve Data", index = False)
    data.to_excel(writer, sheet_name = "Filtered 6 Severe Typhoon" , index = False)
    concat_tideData.to_excel(writer, sheet_name = "Corresponding Tide Data" , index = False)