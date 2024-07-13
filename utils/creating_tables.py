import requests
import pandas as pd
import numpy as np
import time
from functools import wraps

data = pd.read_json("league_standings.json")

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args,**kwargs)
        end_time = time.perf_counter()
        total_time = end_time-start_time
        print(f'function {func.__name__} took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def create_leaguest_table(json_data):
    league_results = pd.DataFrame(data=json_data["standings"]["results"])
    return league_results


#this function takes a player id and returns data compromosing of the gw, the points they got for that gw, and the total points
#NOTE: I can change this so it takes whatever columns we want to it, for various use of data
def getPlayerData(id):
    #importing all relevant league data from 
    all_data = requests.get("https://fantasy.premierleague.com/api/entry/" + str(id) + "/history/").json()
    #convert current from all_data to dataframe
    #checking the keys of dictionary
    #take out the Gw, points and total points
    df_gwPoints = pd.DataFrame(all_data['current'],columns = ['event', 'points', 'total_points'])
    return df_gwPoints

#will build a multi-index table for a league, containing player name, player id, team name, and a multindex of gw(points and total points)
@timeit
def buildTable(league_results):
    players = league_results["player_name"]
    #so this is initalizing the columns
    columns = pd.MultiIndex.from_product([range(1, 38 + 1), ['points', 'total_points']], 
                                         names=['gameweek', 'metric'])# I will hardcode the range for now till I figure out how to decide current GW
    #initializing the df
    df = pd.DataFrame(np.nan, index = players , columns= columns)
    df['player_id'] = np.nan
    df['username'] = np.nan
    #you use zip to iterate over multiple elements in python
    #NOTE: here I am looping through the players ID
    for entry,username, player in zip(league_results["entry"],league_results["entry_name"], players):
        #here I have event, points and total points
        player_hist = getPlayerData(entry)
        #traversing the pd for both points and totalpoints
        idx = player_hist.loc[0,'event'] #idx for gw so each player has their entire row filled
        for points, total_points in zip(player_hist["points"],player_hist["total_points"]):
            df.loc[player,'player_id'] = entry
            df.loc[player,'username'] = username
            df.loc[player, (idx,'points')] = points
            df.loc[player, (idx, 'total_points')] = total_points
            idx = idx + 1
    
    return df


if __name__ == '__main__':
    league_st = create_leaguest_table(data)
    #we will want to save this in the future because this call takes 10 seconds for now
    players_in_league = buildTable(league_st)
    players_in_league.to_pickle('dataframe_players.pkl')

# Load the DataFrame from the Pickle file
    df_multi_loaded = pd.read_pickle('dataframe_players.pkl')