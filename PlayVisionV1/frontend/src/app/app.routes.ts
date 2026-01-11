import { Routes } from '@angular/router';
import { HomePage } from './home-page/home-page';

export const routes: Routes = [
    {
        path: "",
        redirectTo: "home",
        pathMatch: "full",
    },
    {
        path: "home",
        component: HomePage,
    },
    {
        path: "competitions/:competitionName",
        loadComponent: () => import("./competition-page/competition-page").then(m => m.CompetitionPage),
    },
    {
        path: "teams/:teamName",
        loadComponent: () => import("./team-page/team-page").then(m => m.TeamPage),
    },
    {
        path: "players/:playerName",
        loadComponent: () => import("./player-page/player-page").then(m => m.PlayerPage),
    },
    {
        path: "matches/:matchId",
        loadComponent: () => import("./match-page/match-page").then(m => m.MatchPage),
    },
    {
        path: "aboutUs",
        loadComponent: () => import("./about-us-page/about-us-page").then(m => m.AboutUsPage),
    },
    {
        path: "search",
        loadComponent: () => import("./search-page/search-page").then(m => m.SearchPage),
    },
    {
        path: "compare",
        loadComponent: () => import("./compare-page/compare-page").then(m => m.ComparePage),
    },
    {
        path: "**",
        component: HomePage
    },
];
