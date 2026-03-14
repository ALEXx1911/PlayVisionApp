import { Component, input, InputSignal, computed } from '@angular/core';
import { TableModule } from 'primeng/table'
import {  CompetitionDataFromAPI, TeamCompetitionStat } from '../../models/app-models';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'league-table',
  imports: [TableModule, RouterLink],
  templateUrl: './league-table.html',
})
export class LeagueTable{
    readonly data:InputSignal<CompetitionDataFromAPI> = input.required<CompetitionDataFromAPI>();

    readonly teamData = computed((): TeamCompetitionStat[] => this.data()?.team_competition_stats ?? []);

    
}
