import { Component, inject, signal } from '@angular/core';
import { AppService } from '../services/app-service';
import { AsyncPipe } from '@angular/common';
import { RouterLink, RouterLinkActive } from "@angular/router";
import { CdkAccordion, CdkAccordionItem } from "@angular/cdk/accordion";
import { MatIcon } from "@angular/material/icon";

@Component({
  selector: 'app-competition-navbar',
  imports: [AsyncPipe, RouterLink, RouterLinkActive, CdkAccordion, CdkAccordionItem, MatIcon],
  templateUrl: './competition-navbar.html',
  styleUrl: './competition-navbar.css',
})
export class CompetitionNavbar {
  readonly appService = inject(AppService);
  isOpen = signal(false);
  readonly  competitionsData$ = this.appService.getAllCompetitions();

}
