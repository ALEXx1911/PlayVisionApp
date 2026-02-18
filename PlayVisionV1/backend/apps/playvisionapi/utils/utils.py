match_stats_header = [
    {
        "field":"Shots",
        "home_data":"home_shots",
        "away_data":"away_shots"
     },
     {
        "field":"Shots on Target",
        "home_data":"home_shots_ontarget",
        "away_data":"away_shots_ontarget"
     },
     {
        "field":"Corners",
        "home_data":"home_corners",
        "away_data":"away_corners"
     },
     {
        "field":"Possession %",
        "home_data":"home_possession",
        "away_data":"away_possession"
     },
     {
        "field":"Passes",
        "home_data":"home_passes",
        "away_data":"away_passes"
     },
     {
        "field":"Fouls",
        "home_data":"home_fouls",
        "away_data":"away_fouls"
     },
     {
        "field":"Yellow Cards",
        "home_data":"home_yellow_cards",
        "away_data":"away_yellow_cards"
     },
     {
        "field":"Red Cards",
        "home_data":"home_red_cards",
        "away_data":"away_red_cards"
     },
     {
        "field":"Offsides",
        "home_data":"home_offsides",
        "away_data":"away_offsides"
     }

]

def get_last_matches_results(last_five_results, team):
   """ 
   Determines the results of the last five matches for a given team.
   And return a list of results where 'W' stands for a win, 'L' for a loss, and 'D' for a draw. 
   The results are ordered from oldest to most recent.
   """
   results = []
   for match in last_five_results:
       if team.title == match.home_team.title and match.home_goals > match.away_goals:
           results.append('W')
       elif team.title == match.home_team.title and match.home_goals < match.away_goals:
           results.append('L')
       elif team.title == match.away_team.title and match.away_goals > match.home_goals:
           results.append('W')
       elif team.title == match.away_team.title and match.away_goals < match.home_goals:
           results.append('L')
       else:
           results.append('D')
   results.reverse()
   return results

FORMATION_POSITIONS = {
    "4-3-3": [
         "GK",
         "LB", "RCB", "LCB", "RB",
         "LCM", "CDM", "RCM",
         "LW", "DC", "RW"
    ]
}