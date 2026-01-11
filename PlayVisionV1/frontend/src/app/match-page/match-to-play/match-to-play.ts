import { Component, inject, signal } from "@angular/core";
import { ActivatedRoute, RouterLink } from "@angular/router";
import { AppService } from "../../services/app-service";
import { map, switchMap } from "rxjs";
import { AsyncPipe } from "@angular/common";
import { MatchSlot } from "../../competition-page/components/match-slot/match-slot";
import { COLS_HEADERS } from "./utils";

@Component({
    selector: 'app-match-to-play',
    imports: [RouterLink, AsyncPipe, MatchSlot],
    templateUrl: './match-to-play.html',
})
export class MatchToPlay {
    private activeRoute = inject(ActivatedRoute);
    private appService = inject(AppService);
    showHomeLastMatches = signal(true);
    readonly leaguePositionHeaders = COLS_HEADERS;

    toPlayMatchData$ = this.activeRoute.paramMap.pipe(
        map(params => params.get('matchId') ?? ''),
        map(id => parseInt(id, 10)),
        switchMap(id => this.appService.getPreviewMatchDetails(id))
    );

    changeTeamLastMatches(): void {
        this.showHomeLastMatches.set(!this.showHomeLastMatches());
    }
}