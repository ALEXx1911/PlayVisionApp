import { Component, effect, inject, input, signal } from "@angular/core";
import { AppService } from "../../services/app-services/app-service";
import { AsyncPipe } from "@angular/common";
import { asyncScheduler, Observable, scheduled } from "rxjs";
import { PlayerCompareDataFromAPI } from "../../models/app-models";
import { HorizontalBarChart } from "../../player-page/components/horizontal-bar-chart/horizontal-bar-chart";
import { MatIcon } from "@angular/material/icon";

@Component({
    selector: 'app-compare-results',
    imports: [AsyncPipe, HorizontalBarChart, MatIcon],
    templateUrl: './compare-results.html',
})
export class CompareResults {
    readonly appService = inject(AppService);
    player1 = input<string>('');
    player2 = input<string>('');

    compareData$ = signal<Observable<PlayerCompareDataFromAPI>>(scheduled([], asyncScheduler));

    constructor() {
        effect(() => {
            const p1 = this.player1();
            const p2 = this.player2();
            
            if (p1 && p2 && p1.length > 0 && p2.length > 0) {
                this.compareData$.set(this.appService.getPlayerCompareData(p1, p2));
            }
        });
    }
}