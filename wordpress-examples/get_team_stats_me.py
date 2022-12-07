#Import Packages
import os
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import lxml
import time

#Import Helper Functions
from functions import remove_accents

def get_team_stats_me(team, season_end_year, team_current):
  
  r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2F{team}%2F{season_end_year}%2Fgamelog%2F&div=div_tgl_basic')
  

  if r.status_code==200:

    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table')
    if table == None:
      df = 0 
      return df

    df = pd.read_html(str(table))[0]

    #Playoffs
    rp = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2F{team}%2F{season_end_year}%2Fgamelog%2F&div=div_tgl_basic_playoffs')
    if rp.status_code==200:
      soupp = BeautifulSoup(rp.content, 'html.parser')
      tablep = soupp.find('table')
      if tablep != None:
        df_playoffs = pd.read_html(str(tablep))[0]
        df = pd.concat([df, df_playoffs])
    

    df.columns = list(map('_'.join, df.columns.values))

    df = df.iloc[: , [2,3, 4, 5, 6, 7, 10, 27, 22, 39]]

    # print(df.columns)
    df = df.loc[df.iloc[: , 0] != 'Date']
    # df = df.dropna()

    df.columns =  ['Date', 'Venue','Opp', 'Result', 
                   'Tm_score', 'Opp_score', 'Team_FG%', 
                   'Opponent_FG%','Team_TOV','Opponent_TOV']
                   


    df['Winner'],df['Loser'], df['HomeTeam'],df['MOV'] = None, None, None, None
    df['Winner_FG%'],df['Loser_FG%'] =  None, None
    df['Winner_TOV'],df['Loser_TOV'] = None, None

    # #Fill columns of winners and losers 
    df['Winner'].loc[df.Result == 'W'], df['Loser'].loc[df.Result == 'L'] = team_current, team_current
    df['Winner'].loc[df.Result == 'L'] = df['Opp'].loc[df.Result == 'L']
    df['Loser'].loc[df.Result == 'W'] = df['Opp'].loc[df.Result == 'W']

    df['Winner_FG%'].loc[df.Result == 'W'] = df['Team_FG%'].loc[df.Result == 'W']
    df['Winner_FG%'].loc[df.Result == 'L'] = df['Opponent_FG%'].loc[df.Result == 'L']
    df['Loser_FG%'].loc[df.Result == 'L'] = df['Team_FG%'].loc[df.Result == 'L']
    df['Loser_FG%'].loc[df.Result == 'W'] = df['Opponent_FG%'].loc[df.Result == 'W']

    df['Winner_TOV'].loc[df.Result == 'W'] = df['Team_TOV'].loc[df.Result == 'W']
    df['Winner_TOV'].loc[df.Result == 'L'] = df['Opponent_TOV'].loc[df.Result == 'L']
    df['Loser_TOV'].loc[df.Result == 'L'] = df['Team_TOV'].loc[df.Result == 'L']
    df['Loser_TOV'].loc[df.Result == 'W'] = df['Opponent_TOV'].loc[df.Result == 'W']

    #Compute MOV
    df['MOV']  = abs(df[['Tm_score', 'Opp_score']].astype(float).diff(axis=1).iloc[: , -1])


    # #Compute Home team
    df['HomeTeam'].loc[df.Venue != '@'] = team_current
    df['HomeTeam'].loc[df.Venue == '@'] = df['Opp'].loc[df.Venue == '@']

    # #drop columns
    df = df.drop(axis = 1, labels = ['Opp', 'Venue',
                                     'Result', 'Tm_score', 
                                     'Opp_score','Team_FG%', 
                                     'Opponent_FG%','Team_TOV',
                                     'Opponent_TOV'])

  return df