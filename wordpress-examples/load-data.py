#Import Packages
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go

#Import Team Data and helper functions
from constants import TEAM_TO_TEAM_ABBR, TEAM_SETS, CURRENT_TEAM

decades = [1990 + i*10 for i in range(4)] 
filename_list = ['../data/raw/NBA_' + str(decades[i]) + '-'+ str(decades[i+1]) + '_Game-outcomes.csv' for i in range(len(decades) - 1)]

li = []
for filename in filename_list:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

dec = pd.concat(li, axis=0, ignore_index=True)
dec['Date'] = pd.to_datetime(dec['Date'], format="%Y-%m-%d")
