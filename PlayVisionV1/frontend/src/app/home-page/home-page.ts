import { Component, computed, inject } from '@angular/core';
import { AppService } from '../services/app-services/app-service';
import { MatchSlot } from "../competition-page/components/match-slot/match-slot";
import { CdkAccordion, CdkAccordionItem } from "@angular/cdk/accordion";
import { MatIcon } from "@angular/material/icon";
import { StatsTable } from "../competition-page/components/stats-tables/stats-tables";
import { RouterLink } from '@angular/router';
import { FormationPitch } from "../common/formation-pitch/formation-pitch";
import { toSignal } from '@angular/core/rxjs-interop';
import { mapPlayersToFormationSlots } from '../common/formation-pitch/formations';

@Component({
  selector: 'app-home-page',
  imports: [ MatchSlot, RouterLink, CdkAccordion, CdkAccordionItem, MatIcon, StatsTable, FormationPitch],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css',
})
export class HomePage {
    readonly appService = inject(AppService);
    readonly homeData$ = toSignal(this.appService.getHomeData(), { initialValue: null });
    todayDate = new Date().toLocaleDateString();

    playersSlotWithCoords = computed(() => {
      const data = this.homeData$();
      if (!data) return [];
      
      return mapPlayersToFormationSlots('4-3-3', data.top_players_lineup);
    });
    
}
