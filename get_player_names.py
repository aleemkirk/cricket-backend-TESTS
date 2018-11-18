#-->script to get batsman and bowler names from a match
import json, os
from pprint import pprint
import pandas as pd
import xlsxwriter
import xlwt 
from tempfile import TemporaryFile

path_to_json = 'JSON data' #specifying path to the json file directory
pom = list() #list of player of matches
batsmen = list() #list of batsmen
bowlers = list() #list of bowlers
names = list() #list of player names
non_strikers = list() #list of non strikers 

#-->get file names ending with .json
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

#-->reading json file
for file_name in json_files:
    loc = path_to_json+'/'+ file_name #get file location
    with open(loc) as datafile:
        data =json.load(datafile)
    #-->store all player of matches
    if 'player_of_match' not in data['info']:
        pass
    else:
        pom.append(data["info"]["player_of_match"][0])
    #-->store all batsmen, non strikers and bowlers for 1st innings
    if '1st innings' not in data['innings'][0]:
        pass
    else:
        for obj in data['innings'][0]['1st innings']['deliveries']:
            key = list(obj.keys())
            index = key[0]  # get ball number
            if obj[index]['batsman'] not in batsmen:
                batsmen.append(obj[index]['batsman'])
            if obj[index]['bowler'] not in bowlers:
                bowlers.append(obj[index]['bowler'])
            if obj[index]['non_striker'] not in non_strikers:
                non_strikers.append(obj[index]['bowler'])    
    #-->store all batsmen, non strikers and bowlers for 2nd innings
    if '2nd innings' not in data['innings'][len(data['innings'])-1]:
        pass
    else:
        for obj in data['innings'][len(data['innings'])-1]['2nd innings']['deliveries']:
            key = list(obj.keys())
            index = key[0]  # get ball number
            if obj[index]['batsman'] not in batsmen:
                batsmen.append(obj[index]['batsman'])
            if obj[index]['bowler'] not in bowlers:
                bowlers.append(obj[index]['bowler'])
            if obj[index]['non_striker'] not in non_strikers:
                non_strikers.append(obj[index]['bowler'])  
    print(file_name)
#--> creating a list of unique player names
for name in pom:
    if name not in names:
        names.append(name)
for name in batsmen:
    if name not in names:
        names.append(name)
for name in bowlers:
    if name not in names:
        names.append(name)       
for name in non_strikers:
    if name not in names:
        names.append(name)   

print(str(len(names)))

#-->Create excel file with names
header = 'player names'
df = pd.DataFrame({header: names})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("player_names.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Add a header format.
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})

# Write the column headers with the defined format.
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num + 1, value, header_format)

# Close the Pandas Excel writer and output the Excel file.
writer.save()