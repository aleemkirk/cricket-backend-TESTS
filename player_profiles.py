#script to create player profiles using the player_names.xls file and JSON data directory
import json, os
from pprint import pprint
import pandas as pd
import xlwt
import xlrd
from tempfile import TemporaryFile


path_to_json = 'JSON data' #path to the json file 
player_names = list() #store player names 
team = '' #player team
player_of_match = 0
fours = 0
sixes = 0
total_runs = 0
bowled = 0
run_out = 0
caught = 0
wides = 0
match_stats = list() #clear this list every time we look at a new player

#-->Read list of player names from player_names.xls file
df = pd.read_excel('player_names.xlsx') #get column headings
player_names = df[str(df.columns[0])].values #get player names
#-->import json data
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

for player_name in player_names:
    match_stats.clear()
    team = ''
    player_of_match = 0
    for file_name in json_files:
        fours = 0
        sixes = 0
        total_runs = 0
        bowled = 0
        run_out = 0
        caught = 0
        wides = 0
        loc = path_to_json+'/' + file_name
        with open(loc) as datafile:
            data = json.load(datafile)
        
        #-->check if player was player of match
        if 'player_of_match' in data['info']:
            for name in data['info']['player_of_match']:
                if name == player_name:
                    player_of_match += 1
                    break

        #-->checking player stats for 1st innings
        if '1st innings' in data['innings'][0]:
            for obj in data['innings'][0]['1st innings']['deliveries']:
                key = list(obj.keys())
                index = key[0]  # get ball number
                #-->get batting info
                if obj[index]['batsman'] == player_name:
                    #-->check team
                    if data['innings'][0]['1st innings']['team'] != team:
                        team = data['innings'][0]['1st innings']['team']
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
                    if 'extras' in obj[index]:
                        if 'wides' in obj[index]['extras']:
                            wides += obj[index]['extras']['wides']
                    #check for wickets
                    if 'wicket' in obj[index]:
                        if obj[index]['wicket']['kind'] == 'bowled':
                            bowled += 1
                #-->get fielding info
                if 'wicket' in obj[index]:
                    if 'fielders' in obj[index]['wicket']:
                        if obj[index]['wicket']['kind'] == 'caught' and obj[index]['wicket']['fielders'][0] == player_name:
                            caught += 1
                        for fielders in obj[index]['wicket']['fielders']:
                            if obj[index]['wicket']['kind'] == 'run out' and fielders == player_name:
                                run_out += 1
                                break

        #-->check player stats for 2nd innings
        if '2nd innings' in data['innings'][len(data['innings'])-1]:
            for obj in data['innings'][len(data['innings'])-1]['2nd innings']['deliveries']:
                key = list(obj.keys())
                index = key[0]  # get ball number
                #-->get batting info
                if obj[index]['batsman'] == player_name:
                    #-->check team
                    if data['innings'][len(data['innings'])-1]['2nd innings']['team'] != team:
                        team = data['innings'][len(data['innings'])-1]['2nd innings']['team']
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
                    if 'wicket' in obj[index]:
                        if obj[index]['wicket']['kind'] == 'bowled':
                            bowled += 1
                #-->get fielding info
                if 'wicket' in obj[index]:
                    if 'fielders' in obj[index]['wicket']:
                        if obj[index]['wicket']['kind'] == 'caught' and obj[index]['wicket']['fielders'][0] == player_name:
                            caught += 1
                        for fielders in obj[index]['wicket']['fielders']:
                            if obj[index]['wicket']['kind'] == 'run out' and fielders == player_name:
                                run_out += 1
                                break

        #-->placing info into JSON format if player participated in match
        if total_runs + bowled + caught + run_out > 0:
            wickets = {'bowled': bowled, 'run_out': run_out, 'caught': caught}
            match = {'venue': data['info']['venue'], 'date': data['info']['dates'][0], 'fours': fours,
                'sixes': sixes, 'total runs': total_runs, 'wickets': wickets, 'wides': wides}
            match_stats.append(match)

        #-->validating player name
    player_name = player_name.replace('(', '').replace(')', '').replace('\'', '').replace('.', '').replace('-', ' ')

    print(player_name)
    #-->writing player data to external JSON file
    with open('player profiles/' + player_name + '.json', 'w') as outfile:
        json.dump({'player name': player_name,'team' : team, 'player of matches received':player_of_match, 'match stats': match_stats}, outfile, indent=4, sort_keys=False)
