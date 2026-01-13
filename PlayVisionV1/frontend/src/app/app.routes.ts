import { Routes } from '@angular/router';
import { HomePage } from './home-page/home-page';
import { competitionGuard, matchGuard, playerGuard, teamGuard } from './services/route-guards/resource.guard';

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
        canActivate: [competitionGuard],
        loadComponent: () => import("./competition-page/competition-page").then(m => m.CompetitionPage),
    },
    {
        path: "teams/:teamSlug",
        canActivate: [teamGuard],
        loadComponent: () => import("./team-page/team-page").then(m => m.TeamPage),
    },
    {
        path: "players/:playerName",
        canActivate: [playerGuard],
        loadComponent: () => import("./player-page/player-page").then(m => m.PlayerPage),
    },
    {
        path: "matches/:matchId",
        canActivate: [matchGuard],
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
