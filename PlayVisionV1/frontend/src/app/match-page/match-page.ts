import { Component, inject } from '@angular/core';
import { AppService } from '../services/app-services/app-service';
import { AsyncPipe } from '@angular/common';
import { MatchFinished } from "./match-finished/match-finished";
import { MatchToPlay } from "./match-to-play/match-to-play";
import { ActivatedRoute } from '@angular/router';
import { map, switchMap } from 'rxjs';

@Component({
  selector: 'app-match-page',
  imports: [AsyncPipe, MatchFinished, MatchToPlay],
  templateUrl: './match-page.html',
  styleUrl: './match-page.css',
})
export class MatchPage {
  readonly matchService = inject(AppService);
  private routeActivated = inject(ActivatedRoute);

  readonly matchData$ = this.routeActivated.paramMap.pipe(
    map(params => params.get('matchId') ?? ''),
    map(id => parseInt(id, 10)),
    switchMap(id => this.matchService.getMatchDetails(id))
  )
}
