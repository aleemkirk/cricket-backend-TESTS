#test investigating converting python dict to JSON
import json

player_name = 'Aleem Khan'
venue1 = 'stadium 1'
venue2 = 'stadium 2'
date1 = '17/10/1996'
date2 = '1/11/2000'
fours = 0
sixs = 1
total_runs = 6
bowled = 1
run_out = 0
caught = 4
wides = 2

wickets1 = {'bowled':bowled, 'run_out':run_out, 'caught':caught}
wickets2 = {'bowled':bowled, 'run_out':run_out, 'caught':caught}

#creating dummy match data
match1 = {'venue':venue1, 'date':date1, 'fours':fours, 'sixes':sixs, 'total runs':total_runs, 'wickets':wickets1, 'wides':wides}
match2 = {'venue':venue2, 'date':date2, 'fours':fours, 'sixes':sixs, 'total runs':total_runs, 'wickets':wickets2, 'wides':wides}
match_list = [match1, match2]

#writing mock data to external JSON file
with open('mock_player_profile.json', 'w') as outfile:
    json.dump({'player name': player_name, 'match stats':match_list}, outfile, indent=4, sort_keys=False)


