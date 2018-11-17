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
player_name = player_names[0] #delete when implenting final solution 
#-->import json data
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

for player_name in player_names:
    match_stats.clear()
    for file_name in json_files:
        fours = 0
        sixes = 0
        total_runs = 0
        bowled = 0
        run_out = 0
        caught = 0
        wides = 0
        loc = path_to_json+'/'+  file_name
        with open(loc) as datafile:
            data = json.load(datafile)

        for obj in data['innings'][0]['1st innings']['deliveries']:
            for key in obj.keys():
                index =  key  #get ball number
            #-->get batting info
            if obj[index]['batsman'] == player_name:
                #check if four
                if obj[index]['runs']['batsman'] >= 4 and obj[index]['runs']['batsman'] < 6:
                    fours += 1
                #check if six
                if obj[index]['runs']['batsman'] >= 6:
                    sixes += 1
                #check total runs
                total_runs += obj[index]['runs']['batsman']
            #-->get bowling info
            if obj[index]['bowler'] == player_name:
                #check for wides
                if 'extras' not in obj[index]:
                    wides += 0
                else:
                    if 'wides' not in obj[index]['extras']:
                        wides += 0
                    else:
                        wides += obj[index]['extras']['wides']
                #check for wickets
                if 'wicket' not in obj:
                    pass
                else:
                    if obj['wicket']['kind'] == 'bowled':
                        bowled += 1
                #-->get fielding info
                if 'wicket' not in obj:
                    pass
                else:
                    if obj['wicket']['kind'] == 'caught' and obj['wicket']['fielders'][0] == player_name:
                        caught += 1 
                    if obj['wicket']['kind'] == 'run out' and ( obj['wicket']['fielders'][0] == player_name or obj['wicket']['fielders'][1] == player_name ):
                        run_out += 1 
        #-->placing info into JSON format if player participated in match
        if total_runs + bowled + caught + run_out > 0:
            wickets = {'bowled':bowled, 'run_out':run_out, 'caught':caught}
            match = {'venue':data['info']['venue'], 'date':data['info']['dates'][0], 'fours':fours, 'sixes':sixes, 'total runs':total_runs, 'wickets':wickets, 'wides':wides}
            match_stats.append(match)
    #-->writing player data to external JSON file
    newstr = player_name.replace('(', '')
    player_name = newstr.replace(')', '')
    player_name = newstr.replace('\'', '')
    player_name = newstr.replace('.', '')
    player_name = newstr.replace('-', ' ')
    print(player_name)
    with open('player profiles/' + player_name + '.json', 'w') as outfile:
        json.dump({'player name': player_name, 'match stats':match_stats}, outfile, indent=4, sort_keys=False)

