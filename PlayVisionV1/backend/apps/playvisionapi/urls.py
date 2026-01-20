from django.urls import path
from rest_framework import routers
from .api import teams , players , competitions , matches , home , search , most_searched

urlpatterns = [ 
    path("api/home/", home.homepage),
    #URLS for Teams
    path("api/teams/<str:title>/", teams.team_details, name='team-details'),

    #URLS for Competitions
    path("api/competitions/", competitions.competition_list, name='competition-list'),
    path("api/competitions/<str:ctitle>/", competitions.competition_details),
    path("api/competitions/<str:ctitle>/matches/", competitions.competition_matches),

    #URLS for Player
    path("api/players/<str:pname>/", players.player_details),

    #URLS for Matchs
    path("api/matchs/<int:matchid>/", matches.match_details),

    #URLS for Searchs
    path("api/search/", search.search_page),

    #URLS for Compare Players
    path("api/compare/players/", search.compare_players),

    #URLS for Most Searched Items
    path("api/mostsearched/items", most_searched.most_searched_items),
    path("api/mostsearched/players", most_searched.most_searched_players),
]