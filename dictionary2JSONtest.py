#test investigating converting python dict to JSON
import json

player_name = 'Aleem Khan'

bowled = 1
run_out = 0
caught = 4

wickets_json = json.dumps({'bowled':bowled, 'run_out':run_out, 'caught':caught})
print(wickets_json)


json_obj = json.dumps({'Player Name': player_name})
