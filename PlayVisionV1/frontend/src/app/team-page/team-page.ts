import { Component, computed, inject, signal } from '@angular/core';
import { AppService } from '../services/app-service';
import {  switchMap } from 'rxjs';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { TableModule } from 'primeng/table';
import { SkeletonModule } from 'primeng/skeleton';
import { MatchSlot } from "../competition-page/components/match-slot/match-slot";
import { MatIcon } from "@angular/material/icon";
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { FormationPitch } from "../common/formation-pitch/formation-pitch";
import { mapPlayersDataToFormationSlots } from '../common/formation-pitch/formations';

@Component({
  selector: 'app-team-page',
  imports: [TableModule, MatchSlot, SkeletonModule, RouterLink, MatIcon, FormationPitch],
  templateUrl: './team-page.html',
  styleUrl: './team-page.css',
})
export class TeamPage {
  readonly appService = inject(AppService);
  private activatedRoute = inject(ActivatedRoute);
  private routeParams= toSignal(this.activatedRoute.paramMap, { initialValue: null });
  teamName = computed(() => 
    this.routeParams()?.get('teamName') ?? ''
  );
  teamData$ = toSignal(
    toObservable(this.teamName).pipe(
      switchMap((name) => name ? this.appService.getTeamDetails(name) : []),
    ),
    { initialValue: null }
  );

  playerSlotWithCoords = computed(() => {
    const data = this.teamData$();
    if (!data) return [];

    return mapPlayersDataToFormationSlots(data.team.preferred_formation, data.player_stats);
  });

}

