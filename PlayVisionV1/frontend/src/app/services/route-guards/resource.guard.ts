// src/app/services/route-guards/resource.guard.ts
import { Injectable, inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AppService } from '../app-services/app-service';
import { catchError, map, of } from 'rxjs';

export const teamGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const appService = inject(AppService);
  const teamSlug = route.paramMap.get('teamSlug');

  if (!teamSlug) {
    //console.warn('Team guard: teamSlug parameter is missing.');
    router.navigate(['/home']);
    return false;
  }

  return appService.getTeamDetails(teamSlug).pipe(
    map((data) => {
      //console.log('Team found:', data);
      return true;
    }),
    catchError((error) => {
      //console.error('Team guard error:', error, 'for teamSlug:', teamSlug);
      router.navigate(['/home']);
      return of(false);
    })
  );
};
export const competitionGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const appService = inject(AppService);
  const competitionSlug = route.paramMap.get('competitionSlug');

  if (!competitionSlug) {
    //console.warn('Competition guard: competitionSlug parameter is missing.');
    router.navigate(['/home']);
    return false;
  }

  return appService.getCompetitionDetails(competitionSlug).pipe(
    map((data) => {
      //console.log('Competition found:', data);
      return true;
    }),
    catchError((error) => {
      //console.error('Competition guard error:', error, 'for competitionSlug:', competitionSlug);
      router.navigate(['/home']);
      return of(false);
    })
  );
};

export const playerGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const appService = inject(AppService);
  const playerName = route.paramMap.get('playerName');

  if (!playerName) {
    router.navigate(['/home']);
    return false;
  }

  return appService.getPlayerDetails(playerName).pipe(
    map(() => true),
    catchError(() => {
      router.navigate(['/home']);
      return of(false);
    })
  );
};

export const matchGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const appService = inject(AppService);
  const matchId = route.paramMap.get('matchId');

  if (!matchId || isNaN(parseInt(matchId))) {
    router.navigate(['/home']);
    return false;
  }

  return appService.getMatchDetails(parseInt(matchId)).pipe(
    map(() => true),
    catchError(() => {
      router.navigate(['/home']);
      return of(false);
    })
  );
};