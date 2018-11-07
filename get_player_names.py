#-->script to get batsman and bowler names from a match
import json, os
from pprint import pprint
import pandas as pd

path_to_json = 'JSON data' #specifying path to the json file directory
pom = list() #list of player of matches
batsmen = list() #list of batsmen
bowlers = list() #list of bowlers
names = list() #list of player names

#-->get file names ending with .json
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

#-->reading json file
for name in json_files:
    loc = path_to_json+'/'+ name #get file location
    with open(loc) as datafile:
        data =json.load(datafile)
    #-->store all player of matches
    if 'player_of_match' not in data['info']:
        pom.append('')
    else:
        pom.append(data["info"]["player_of_match"])
    #-->store all batsmen and bowlers for 1st innings
    if '1st innings' not in data['innings']:
        batsmen.append('')
        bowlers.append('')
    #-->stor all batsmen and bowlers for 2nd innings
    if '2nd innings' not in data['innings']:
        batsmen.append('')
        bowlers.append('')
    

#--> creating a list of player names
for name in pom:
    if name not in names:   #store if name not already in list
        if len(name) == 1:  #only store name if there was one POM
            names.append(name)

print(len(names))