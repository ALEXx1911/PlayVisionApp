from django.urls import path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .api import teams , players , competitions , matches , home , search , most_searched

urlpatterns = [ 
    path("api/v1/home/", home.homepage, name='home-page'),
    #URLS for Teams
    path("api/v1/teams/<str:title>/", teams.team_details, name='team-details'),

    #URLS for Competitions
    path("api/v1/competitions/", competitions.competition_list, name='competitions-list'),
    path("api/v1/competitions/<str:ctitle>/", competitions.competition_details, name='competition-details'),
    path("api/v1/competitions/<str:ctitle>/matches/", competitions.competition_matches),

    #URLS for Player
    path("api/v1/players/<str:pname>/", players.player_details, name='player-details'),

    #URLS for Matches
    path("api/v1/matches/<int:matchid>/", matches.match_details, name='match-details'),

    #URLS for Searchs
    path("api/v1/search/", search.search_page, name='search-page'),

    #URLS for Compare Players
    path("api/v1/compare/players/", search.compare_players, name='compare-players'),

    #URLS for Most Searched Items
    path("api/v1/mostsearched/items", most_searched.most_searched_items),
    path("api/v1/mostsearched/players", most_searched.most_searched_players),

    #URLS for Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]