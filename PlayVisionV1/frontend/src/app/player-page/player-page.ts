import { Component, inject, signal } from '@angular/core';
import { AppService } from '../services/app-services/app-service';
import { ActivatedRoute } from '@angular/router';
import { map, Observable, switchMap } from 'rxjs';
import { PlayerDataFromAPI, PlayerStat } from '../models/app-models';
import { AsyncPipe } from '@angular/common';
import { ChartModule } from 'primeng/chart';
import { CdkAccordion, CdkAccordionItem } from "@angular/cdk/accordion";
import { MatIcon } from "@angular/material/icon";
import { TableModule } from "primeng/table";
import { HorizontalBarChart } from "./components/horizontal-bar-chart/horizontal-bar-chart";

@Component({
  selector: 'app-player-page',
  imports: [AsyncPipe, ChartModule, CdkAccordion, CdkAccordionItem, MatIcon, TableModule, HorizontalBarChart],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css',
})
export class PlayerPage {
  readonly appService = inject(AppService);
  private activatedRoute = inject(ActivatedRoute);
  chartData: any;
  playerName = signal('');
  playerData$: Observable<PlayerDataFromAPI> = this.activatedRoute.paramMap.pipe(
    map(params => params.get('playerName') ?? ''),
    map(name => {this.playerName.set(name); return name;}),
    switchMap(name => this.appService.getPlayerDetails(name))
  );
  datalabels: Array<keyof PlayerStat> = ['matches_played','goals','assists','correctpassesmedia','tackles','yellow_cards','red_cards','cleansheets'];
}
