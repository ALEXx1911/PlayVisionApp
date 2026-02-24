import { Component, computed, input, InputSignal } from "@angular/core";
import { TableModule } from "primeng/table";
import { RouterLink } from "@angular/router";
import { MostYellowCardData, TopGoalkeeperData, TopMediaPlayerData, TopScorersData } from "../../../models/player-models/player-models";

@Component({
    selector: 'stats-tables',
    imports: [TableModule,RouterLink],
    templateUrl: './stats-tables.html',
})
export class StatsTable{
    readonly topScorersData: InputSignal<TopScorersData[]> = input.required<TopScorersData[]>();
    readonly mostYellowCardData: InputSignal<MostYellowCardData[]> = input.required<MostYellowCardData[]>();
    readonly topMediaPlayersData: InputSignal<TopMediaPlayerData[]> = input.required<TopMediaPlayerData[]>();
    readonly topGoalkeepersData: InputSignal<TopGoalkeeperData[]> = input.required<TopGoalkeeperData[]>();
    
    readonly scorersStats = computed((): TopScorersData[] => this.topScorersData() ?? []);
    readonly yellowCardsStats = computed((): MostYellowCardData[] => this.mostYellowCardData() ?? []);
    readonly mediaPlayerStats = computed((): TopMediaPlayerData[] => this.topMediaPlayersData() ?? []);
    readonly goalkeepersStats = computed((): TopGoalkeeperData[] => this.topGoalkeepersData() ?? []);
    
}