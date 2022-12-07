#Initialise the elo
elo = {team[0] : [] for team in CURRENT_TEAM}
starting_elo = 1000

for team in CURRENT_TEAM:
  start = min(dec["Date"].loc[dec["Winner"] == team[0]].min(),dec["Date"].loc[dec["Loser"] == team[0]].min()) - timedelta(days=1)
  elo[team[0]].append([start, starting_elo])

dec = dec.dropna()

#Replace old names
replace_key = {}
for i in range(len(TEAM_SETS)):
  for old_name in TEAM_SETS[i]:
    replace_key[old_name] = CURRENT_TEAM[i]

dec = dec.replace({col:replace_key for col in ["Winner", "Loser", "HomeTeam"]})


#Define ELO Functions

def expected_outcome(elo_a,elo_b,m):
  #returns E_A
  return 1/(1 + 10**((elo_b - elo_a)/m))

def update_elo(elo_a, elo_b, s_a, k, m):
  return (elo_a + k*(s_a - expected_outcome(elo_a,elo_b,m)))


def elo_formula(game, elo,k = 10,m = 400):
  winner = game['Winner']
  loser = game['Loser']
  date = game['Date']

  winner_elo = elo[winner][-1][1]
  loser_elo = elo[loser][-1][1]
  
  winner_elo_new = update_elo(winner_elo, loser_elo, 1, k, m)
  loser_elo_new = update_elo(loser_elo, winner_elo, 0, k, m)

  elo[winner].append([date, winner_elo_new])
  elo[loser].append([date, loser_elo_new])

  return elo