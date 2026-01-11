import { Component, computed, input, InputSignal } from "@angular/core";
import { TableModule } from "primeng/table";
import { PlayerStat } from "../../models/competition-models";
import { RouterLink } from "@angular/router";

@Component({
    selector: 'stats-tables',
    imports: [TableModule,RouterLink],
    templateUrl: './stats-tables.html',
})
export class StatsTable{
    readonly topScorersData: InputSignal<PlayerStat[]> = input.required<PlayerStat[]>();
    readonly mostYellowCardData: InputSignal<PlayerStat[]> = input.required<PlayerStat[]>();
    readonly topMediaPlayersData: InputSignal<PlayerStat[]> = input.required<PlayerStat[]>();
    readonly topGoalkeepersData: InputSignal<PlayerStat[]> = input.required<PlayerStat[]>();
    
    readonly scorersStats = computed((): PlayerStat[] => this.topScorersData() ?? []);
    readonly yellowCardsStats = computed((): PlayerStat[] => this.mostYellowCardData() ?? []);
    readonly mediaPlayerStats = computed((): PlayerStat[] => this.topMediaPlayersData() ?? []);
    readonly goalkeepersStats = computed((): PlayerStat[] => this.topGoalkeepersData() ?? []);
    
}