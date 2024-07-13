import requests, json
from pprint import pprint
import pandas as pd

# define API endpoint & get data ...
base_url = 'https://fantasy.premierleague.com/api/' 
r_lg = requests.get(base_url+'leagues-classic/452471/standings/').json() 

# save dawnloaded data to json file ...
with open('league_standings.json', 'w') as file:
    json.dump(r_lg, file, indent=4)


pl_lg = requests.get("https://fantasy.premierleague.com/api/entry/9035684/history/").json() # the.json() will return a dictionary

with open('player_data2.json','w') as file:
    json.dump(pl_lg, file, indent = 4)
    
current_df = pd.DataFrame(pl_lg["current"])

# Select the first three columns
current_season = current_df.iloc[:, :3]

# Display the result
print(current_season)
