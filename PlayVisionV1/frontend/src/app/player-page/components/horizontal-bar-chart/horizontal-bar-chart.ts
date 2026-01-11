import { Component, input } from "@angular/core";
import { PlayerStatBasic } from "../../../models/app-models";

@Component({
    selector : 'app-horizontal-bar-chart',
    imports: [],
    templateUrl: './horizontal-bar-chart.html',
})
export class HorizontalBarChart {
    playerData = input<PlayerStatBasic>({
        matches_played: 0,
        goals: 0,
        assists: 0,
        correctpassesmedia: 0,
        tackles: 0,
        yellow_cards: 0,
        red_cards: 0,
        cleansheets: 0,
    } as PlayerStatBasic);

    normalizeMatchesPlayedData(data: number): number {
    const maxDataValue = 90; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
  normalizeGoalsData(data: number): number {
    const maxDataValue = 90; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
    normalizeAssistsData(data: number): number {
    const maxDataValue = 60; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
    normalizeCorrectPassesData(data: number): number {
    const maxDataValue = 100; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
    normalizeTacklesData(data: number): number {
    const maxDataValue = 80; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
    normalizeYellowCardsData(data: number): number {
    const maxDataValue = 30; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
    normalizeRedCardsData(data: number): number {
    const maxDataValue = 20; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
    normalizeCleansheetsData(data: number): number {
    const maxDataValue = 50; 
    if(!data || data <=0 ) return 0;
    return (data / maxDataValue) * 100;
  }
}