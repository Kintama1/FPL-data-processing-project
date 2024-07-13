import pandas as pd
import matplotlib.pyplot as plt
import requests, json
import os
import numpy as np
#I am reading the data that I saved from the .json
data = pd.read_json("league_standings.json")
#making a general df which is really not nessecary, should amend this                         
general_df = pd.DataFrame(data)
league_results = pd.DataFrame(general_df["standings"]["results"])

#Afterwards this can be edited to get the raw data as a method and other methods will implement it to get the data they need, 
#for now let's stick with visualizaiton goal

def getPlayerData(id):
    #importing all relevant league data from 
    all_data = requests.get("https://fantasy.premierleague.com/api/entry/" + str(id) + "/history/").json()
    #convert current from all_data to dataframe
    df_all_data = pd.DataFrame(all_data["current"])
    #take out the Gw, points and total points
    df_gwPoints = df_all_data.iloc[:,:3]
    return df_gwPoints

#this builds the pd table of players, current gw and total gw from the data
def buildTable():
    players = league_results["player_name"]
    #so this is initalizing the columns
    columns = pd.MultiIndex.from_product([range(1, 38 + 1), ['points', 'total_points']], 
                                         names=['gameweek', 'metric'])# I will hardcode the range for now till I figure out how to decide current GW
    #initializing the df
    df = pd.DataFrame(np.nan, index = players , columns= columns)
    #you use zip to iterate over multiple elements in python
    #NOTE: here I am looping through the players ID
    for entry, player in zip(league_results["entry"], players):
        #here I have event, points and total points
        player_hist = getPlayerData(entry)
        #traversing the pd for both points and totalpoints
        idx = player_hist["event"].loc[0] #idx for gw so each player has their entire row filled
        for points, total_points in zip(player_hist["points"],player_hist["total_points"]):
            df.loc[player, (idx,'points')] = points
            df.loc[player, (idx, 'total_points')] = total_points
            idx = idx + 1
    
    return df

#saving the players table to a pkl file
def savetable(df, filename = "players_table.pkl"):
    df.to_pickle(filename)

#loading the players table from pkl file if it exits (otherwise it returns none)
def loadtable(filename = "players_table.pkl"):
    if os.path.exists(filename):
        return pd.read_pickle(filename)
    else: 
        return None

#intializing filename
filename = "players_table.pkl"

players_table = loadtable(filename)

#condition if player_table not loaded
if players_table is None:
    players_table = buildTable()
    savetable(players_table, filename)


#method that draws a plot of the progression of two players (starter method, will edit it to include multiple players at some point)
def two_player_comp(name1, name2):
    #chatGPT fed me this so I went down a rabbit hole to understand multi-level indexing(rabbit hole is reading pandas documentation)
    total_player1 = players_table.loc[name1, (slice(None), "total_points")]
    #essentially, loc[name of row(which is player name as label indec),(elements to select from level 1 column(all elements since slice none)), element from level 2(here specified for total_points)]
    total_player2 = players_table.loc[name2, (slice(None), "total_points")]#I finally got it after reading all about loc/multi-index lables and finally slice(none)
    x_points = list(range(1,39))
    plt.plot(x_points,total_player1, c= "red", label= name1)
    plt.plot(x_points,total_player2, c = "blue", label = name2)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

#method that allows for drawing the bar graoh for a particular gameweek for that league
def gw_bar(gw):
    #getting a series of the gw 
    gw_points = players_table.xs((gw, "points"), level = ('gameweek', 'metric'), 
                                 axis = 1).sort_values(by = (gw, "points") , ascending= False)
    #making a list out of the points gotten for processing
    gw_points_list = gw_points.to_numpy().flatten().tolist()
    #getting list of names for x-row
    players_names = gw_points.index
    #plotting
    fig, ax = plt.subplots()
    ax.bar(players_names, gw_points_list)
    ax.set_xlabel('Names')
    ax.set_ylabel('Points')
    ax.set_title(f'Bar graph for GW {gw} points')
    ax.grid(True)

    #rotates names 90 degrees
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show()

#ehehehe I am proud of this one because of the loop, it visualizes a comparison between a gameweek and the previous one
def two_gws_bars(gw):
    index_slice = pd.IndexSlice
    #slicing the data for the given gw and the previous one
    current_gw_points =players_table.loc[:, index_slice[[gw, gw-1], 
                                'points']].sort_values(by = (gw, "points") , ascending= False)
    #returns a list of index of the players names
    players_names = current_gw_points.index
    #list of points for current gw
    current_gw_points_list = current_gw_points.loc[:,gw].to_numpy().flatten().tolist()
    #list of points of previous gw
    previous_gw_points_list = current_gw_points.loc[:,gw-1].to_numpy().flatten().tolist()
    #drawing the subplot
    fig, ax = plt.subplots()
    #lableling the legends
    legend_labels = [f'GW {gw-1} Points', f'GW {gw} Points']
    #gwp for gw previous, gwc for gw current and name for names of players
    for gwp, gwc, name in zip(previous_gw_points_list,current_gw_points_list,players_names):
        if gwp > gwc:
            ax.bar(name, gwc, color = 'blue')
            new_gwp = gwp - gwc
            ax.bar(name, new_gwp, color = 'orange',bottom = gwc)
        elif gwc > gwp:
            ax.bar(name, gwp, color = 'orange')
            new_gwc =gwc - gwp
            ax.bar(name, new_gwc,color = 'blue', bottom  = gwp)
        else:
            ax.bar(name, gwc, color = 'blue')
    
    #naming the axis, title and showing grid of graph
    ax.set_xlabel("Players name")
    ax.set_ylabel("Points")
    ax.legend(legend_labels, loc ="upper right")
    ax.set_title(f'bar graph for GW {gw} compared to GW{gw-1}')
    ax.grid(True)

    #rotating names 90degrees for visibilit
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show()


two_player_comp('Adi Pall-Pareek', 'Fotis Zafiriou')


