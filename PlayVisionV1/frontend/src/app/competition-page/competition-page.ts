import { Component, computed, ElementRef, inject, signal, ViewChild } from '@angular/core';
import { AppService } from '../services/app-services/app-service';
import { LeagueTable } from "../common/components/league-table";
import { CompetitionDataFromAPI, Match, TeamCompetitionStat } from '../models/app-models';
import { CdkAccordionModule } from '@angular/cdk/accordion';
import { MatIcon } from "@angular/material/icon";
import { StatsTable } from "../common/components/stats-tables/stats-tables";
import { switchMap } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { TableModule } from "primeng/table";
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { Skeleton } from "primeng/skeleton";
import { SimpleMatchSlot } from '../common/components/simple-match-slot/simple-match-slot';

@Component({
  selector: 'app-competition',
  imports: [LeagueTable, CdkAccordionModule, MatIcon, StatsTable, TableModule, SimpleMatchSlot, Skeleton],
  templateUrl: './competition.html',
  styleUrl: './competition.css',
})
export class CompetitionPage {
  readonly competitionService = inject(AppService);
  readonly activatedRoute = inject(ActivatedRoute);
  private routeParams = toSignal(this.activatedRoute.paramMap, { initialValue: null });
  competitionSlug = computed(() => {
    return this.routeParams()?.get('competitionSlug') ?? '';
  });
  //Ensures that when the route parameter changes, the competition data is fetched accordingly
  competitionData$ = toSignal(
    toObservable(this.competitionSlug).pipe(
      switchMap(slug => slug ? this.competitionService.getCompetitionDetails(slug) : []),
    ),
    { initialValue: null }
  );

  matches = signal<Match[]>([]);
  loading = signal(false);
  hasMore = signal(true);
  private currentOffset = 0;
  private readonly LIMIT = 10;

  loadMoreMatches(){
    const slug = this.competitionSlug();

    if (!slug || this.loading() || !this.hasMore()) return;

    this.loading.set(true);

    this.competitionService.getCompetitionMatches(slug, this.currentOffset, this.LIMIT)
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

  @ViewChild('scrollContainer') scrollContainer!: ElementRef;

  onScroll(event:any){
    const element = event.target;
    const atBottom = element.scrollHeight - element.scrollTop === element.clientHeight;

    if (atBottom && this.hasMore() && !this.loading()) {
      this.loadMoreMatches();
    }
  }

  
  readonly eje:CompetitionDataFromAPI;

  constructor(){


    this.eje = { 
      competition_data: { id: 1, 
        title: "Liga", 
        slug: "liga", 
        country : "spain", 
        competition_type: "league", 
        logo_url:"xd"  
      } ,
    team_competition_stats: [] as TeamCompetitionStat[], 
    top_scorers: [] as any[],
    most_yellow_cards: [] as any[],
    top_media_players: [] as any[],
    top_goalkeepers: [] as any[]};
  }

}