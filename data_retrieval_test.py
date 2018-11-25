#script to create player profiles using the player_names.xls file and JSON data directory
import json, os
from pprint import pprint
import pandas as pd
import xlwt
import xlrd
from tempfile import TemporaryFile


path_to_json = 'JSON data' #path to the json file 
player_names = list() #store player names 
fours = 0
sixes = 0
total_runs = 0
bowled = 0
run_out = 0
caught = 0
wides = 0
match_stats = list() #clear this list every time we look at a new player
#-->temp vars. Change when implemting final full solution
player_name = ''

#-->Read list of player names from player_names.xls file
df = pd.read_excel('player_names.xlsx') #get column headings
player_names = df[str(df.columns[0])].values #get player names
player_name = player_names[756] #delete when implenting final solution 
#-->import json data
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
loc = path_to_json+'/' + json_files[0]
with open(loc) as datafile:
    data = json.load(datafile)

print(json_files[0])

for obj in data['innings'][0]['1st innings']['deliveries']:
    ball = list(obj.keys())[0]
    if 'wicket' in obj[ball]:
        if obj[ball]['wicket']['kind'] != 'bowled':
            print(str(ball) + ' ' + str(obj[ball]['wicket']['fielders'][0]))

