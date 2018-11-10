#script to create player profiles using the player_names.xls file and JSON data directory
import json, os
from pprint import pprint
import pandas as pd
import xlwt
import xlrd
from tempfile import TemporaryFile

path_to_json = 'JSON data' #specifying path to the json file directory
player_names = list() #store player names

#-->Read list of player names from player_names.xls file
df = pd.read_excel('player_names.xlsx') #get column headings
player_names = df[str(df.columns[0])].values #get player names

#-->import json data
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
loc = path_to_json+'/'+ json_files[0] 
print(json_files[0])
print(player_names[0])

with open(loc) as datafile:
    data = json.load(datafile)

for obj in data['innings'][0]['1st innings']['deliveries']:
    for key in obj.keys():
        index =  key  #get ball number
    if obj[index]['batsman'] == player_names[0]:
        print(index + ': '+ player_names[0] + ' : runs: ' + str(obj[index]['runs']['batsman']))

