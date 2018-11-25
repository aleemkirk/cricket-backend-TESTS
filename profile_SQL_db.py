#creating SQL database of player profile information using the 'player profiles' dir
import json, os
import pymysql

db_name = 'cricket_player_profiles'
db_user = 'root'
db_password = ''
directory = 'player profiles/' #directory of JSON player profile information
player_names = list()

    
#-->accesing SQL database
connection = pymysql.connect(
    host = 'localhost',
    user = db_user,
    passwd = db_password,
    db = db_name
)

if connection:
    print('Connection Succesful')

try:
    with connection.cursor() as cursor:
        #-->Create table 
        sqlQuery = "CREATE TABLE `Players`(id int PRIMARY KEY, Name varchar(32), Team varchar(32), Player_of_matches_received int);"
        cursor.execute(sqlQuery)
        #-->reading in each file from the 'player profiles' dir and getting player general information
        json_files = [pos_json for pos_json in os.listdir(directory) if pos_json.endswith('.json')] #reading all files in JSON dir
        player_id = 0
        for player_file in json_files:
            location = directory + player_file
            with open(location) as datafile:
                data = json.load(datafile)
            player_name = data['player name']
            player_team = data['team']
            player_of_matches_received = data['player of matches received']
            #sqlQuery = "INSERT INTO Players(id, Name,Team,Player_of_matches_received) VALUES("+str(player_id)+",\""+player_name+"\",\""+player_team+"\","+str(player_of_matches_received)+");"
            sqlQuery = "INSERT INTO `players` (`id`, `Name`, `Team`, `Player_of_matches_received`) VALUES ('"+str(player_id)+"', '"+player_name +"', '"+ player_team+"', '"+str(player_of_matches_received) +"');"
            cursor.execute(sqlQuery)
            connection.commit()
            player_id += 1
            #-->Creating and populate match stats table for each player
            player_name = player_name.replace(' ' ,'_')
            sqlQuery = "CREATE TABLE `"+ str(player_name) +"`(id int PRIMARY KEY, venue varchar(64), date varchar(64), fours int, sixes int, total_runs int, bowled int, run_out int, caught int, wides int);"
            cursor.execute(sqlQuery)
            connection.commit()
            player_match_id = 0
            for match in data['match stats']:
                sqlQuery = "INSERT INTO `"+ str(player_name) +"` (`id`, `venue`, `date`, `fours`, `sixes`, `total_runs`, `bowled`, `run_out`, `caught`, `wides`) VALUES ('"+str(player_match_id)+"', '"+match['venue'].replace('\'', '/') +"', '"+ match['date']+"', '"+str(match['fours']) +"', '"+str(match['sixes']) +"', '"+str(match['total runs']) +"', '"+str(match['wickets']['bowled']) +"', '"+str(match['wickets']['run_out']) +"', '"+str(match['wickets']['caught']) +"', '"+str(match['wides']) +"');"
                cursor.execute(sqlQuery)
                connection.commit()
                player_match_id += 1
            print(player_name)
except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connection.close()
#-->TODO create table of player names and stats