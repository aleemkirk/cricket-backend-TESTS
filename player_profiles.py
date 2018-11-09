#script to create player profiles using the player_names.xls file and JSON data directory
import json, os
from pprint import pprint
import pandas as pd
import xlwt
import xlrd
from tempfile import TemporaryFile


player_names = list() #store player names

#-->Read list of player names from player_names.xls file
df = pd.read_excel('player_names.xlsx') #get column headings
player_names = df[str(df.columns[0])].values #get player names
print(player_names)