import { Component, computed, ElementRef, inject, signal, ViewChild } from '@angular/core';
import { AppService } from '../services/app-services/app-service';
import {  switchMap } from 'rxjs';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { TableModule } from 'primeng/table';
import { SkeletonModule } from 'primeng/skeleton';
import { HomeMatchSlot } from "../competition-page/components/home-match-slot/home-match-slot";
import { MatIcon } from "@angular/material/icon";
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { FormationPitch } from "../common/formation-pitch/formation-pitch";
import { mapPlayersDataToFormationSlots } from '../common/formation-pitch/formations';
import { Match } from '../models/app-models';

@Component({
  selector: 'app-team-page',
  imports: [TableModule, HomeMatchSlot, SkeletonModule, RouterLink, MatIcon, FormationPitch],
  templateUrl: './team-page.html',
  styleUrl: './team-page.css',
})
export class TeamPage {
  readonly appService = inject(AppService);
  private activatedRoute = inject(ActivatedRoute);
  private routeParams= toSignal(this.activatedRoute.paramMap, { initialValue: null });
  teamSlug = computed(() => 
    this.routeParams()?.get('teamSlug') ?? ''
  );
  teamData$ = toSignal(
    toObservable(this.teamSlug).pipe(
      switchMap((slug) => slug ? this.appService.getTeamDetails(slug) : []),
    ),
    { initialValue: null }
  );

  matches = signal<Match[]>([]);
  loading = signal(false);
  hasMore = signal(true);
  private currentOffset = 0;
  private readonly LIMIT = 10;

  loadMoreMatches(){
    const slug = this.teamSlug();

    if (!slug || this.loading() || !this.hasMore()) return;

    this.loading.set(true);

    this.appService.getTeamMatches(slug, this.currentOffset, this.LIMIT)
    .subscribe({
      next: (response) => {
        this.matches.update(current => [...current, ...response.matches]);
        this.hasMore.set(response.has_more);
        this.currentOffset += this.LIMIT;
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }

  ngOnInit(){
    this.loadMoreMatches();
  }

  playerSlotWithCoords = computed(() => {
    const data = this.teamData$();
    if (!data) return [];

    return mapPlayersDataToFormationSlots(
      data.team.preferred_formation, 
      data.team_lineup
    );
  });

  @ViewChild('scrollContainer') scrollContainer!: ElementRef;
  
  onScroll(event:any){
    const element = event.target;
    const atBottom = element.scrollHeight - element.scrollTop === element.clientHeight;

    if (atBottom && this.hasMore() && !this.loading()) {
      this.loadMoreMatches();
    }
  }

}

