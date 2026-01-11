import { Component, input, InputSignal, computed } from '@angular/core';
import { TableModule } from 'primeng/table'
import {  DataFromCompetitionAPI, TeamCompetitionStat } from '../models/competition-models';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'league-table',
  imports: [TableModule, RouterLink],
  templateUrl: './league-table.html',
})
export class LeagueTable{
    readonly data:InputSignal<DataFromCompetitionAPI> = input.required<DataFromCompetitionAPI>();

    readonly teamData = computed((): TeamCompetitionStat[] => this.data()?.competition.team_competition_stats ?? []);

    
}
