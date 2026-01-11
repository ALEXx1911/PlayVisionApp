from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [ 
    path("api/home/", views.homepage),
    #URLS for Teams
    path("api/teams/<str:title>/", views.team_details),
    #URLS for Competitions
    path("api/competitions/", views.competition_list),
    path("api/competitions/<str:ctitle>/", views.competition_details),
    path("api/competitions/<str:ctitle>/matches/", views.competition_matches),
    #URLS for Player
    path("api/players/<str:pname>/", views.player_details),
    #URLS for Matchs
    path("api/matchs/<int:matchid>/", views.match_details),
    #URLS for Searchs
    path("api/search/", views.search_page),
    #URLS for Compare Players
    path("api/compare/players/", views.compare_players),
    #URLS for Most Searched Items
    path("api/mostsearched/items", views.most_searched_items),
    path("api/mostsearched/players", views.most_searched_players),
]