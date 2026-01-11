import { Component, inject, signal } from '@angular/core';
import { AppService } from '../services/app-service';
import { LeagueTable } from "./components/league-table";
import { AsyncPipe } from '@angular/common';
import { CompetitionMatchesFromAPI, DataFromCompetitionAPI, Match, TeamCompetitionStat } from '../models/app-models';
import {CdkAccordionModule } from '@angular/cdk/accordion';
import { MatIcon } from "@angular/material/icon";
import { StatsTable } from "./components/stats-tables/stats-tables";
import { map, Observable, switchMap } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import {  TableModule } from "primeng/table";
import { MatchSlot } from "./components/match-slot/match-slot";

@Component({
  selector: 'app-competition',
  imports: [LeagueTable, AsyncPipe, CdkAccordionModule, MatIcon, StatsTable, TableModule, MatchSlot],
  templateUrl: './competition.html',
  styleUrl: './competition.css',
})
export class CompetitionPage {
  readonly competitionService = inject(AppService);
  readonly activatedRoute = inject(ActivatedRoute);
  readonly rows = 20;
  readonly rowHeight = 40;
  competitionName = signal('');
  //Asegurar de que este componente siempre se pase
  competitionData$: Observable<DataFromCompetitionAPI> = this.activatedRoute.paramMap.pipe(
      map(params => params.get('competitionName') ?? ''),
      map(name => {this.competitionName.set(name); return name;}),
      switchMap(name => this.competitionService.getCompetitionDetails(name))
    );

  competitionMatches$: Observable<CompetitionMatchesFromAPI> = this.activatedRoute.paramMap.pipe(
    map(params => params.get('competitionName') ?? ''),
    map(name => {this.competitionName.set(name); return name;}),
    switchMap(name => this.competitionService.getCompetitionMatches(name,0,this.rows))
  );
  
  matches = Array.from<Match>({length:0});

  
  readonly eje:DataFromCompetitionAPI;

  constructor(){


    this.eje = { competition: { id: 1, title: "Liga", slug: "liga", country : "spain", competition_type: "league", logo_url:"xd",  team_competition_stats: [] as TeamCompetitionStat[] } ,
    top_scorers: [] as any[],
    most_yellow_cards: [] as any[],
    top_media_players: [] as any[],
    top_goalkeepers: [] as any[]};
  }

}