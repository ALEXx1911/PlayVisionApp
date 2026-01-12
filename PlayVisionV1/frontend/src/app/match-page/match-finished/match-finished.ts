import { Component, inject, input, InputSignal, signal } from "@angular/core";
import { CdkAccordion, CdkAccordionItem } from "@angular/cdk/accordion";
import { MatIcon } from "@angular/material/icon";
import { ActivatedRoute, RouterLink } from "@angular/router";
import { AsyncPipe } from "@angular/common";
import { FinishedMatchFromAPI, MatchDataFromAPI } from "../../models/app-models";
import { AppService } from "../../services/app-services/app-service";
import { map, Observable, switchMap } from "rxjs";

@Component({
    selector: 'app-match-finished',
    imports: [RouterLink,CdkAccordion, CdkAccordionItem, MatIcon, AsyncPipe],
    templateUrl: './match-finished.html',
})
export class MatchFinished {
    readonly appService = inject(AppService);
    private activeRoute = inject(ActivatedRoute);
    showPlayersChanges = signal(false);

    readonly matchData: InputSignal<MatchDataFromAPI> = input.required<MatchDataFromAPI>();

    finishedMatch$: Observable<FinishedMatchFromAPI> = this.activeRoute.paramMap.pipe(
        map(params => params.get('matchId') ?? ''),
        map(id => parseInt(id, 10)),
        switchMap(id => this.appService.getFinishedMatchDetails(id))
    );

    changePlayersChangesVisibility(): void {
        this.showPlayersChanges.set(!this.showPlayersChanges());
    }

}