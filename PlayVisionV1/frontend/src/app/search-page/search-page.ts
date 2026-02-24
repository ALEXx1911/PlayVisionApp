import { Component, inject, signal } from '@angular/core';
import { AppService } from '../services/app-services/app-service';
import {  ReactiveFormsModule } from '@angular/forms';
import { OverlayModule } from "@angular/cdk/overlay";
import { Competition, SearchTermsData, } from '../models/app-models';
import { SearchBar } from "./components/search-bar/search-bar";
import { RouterLink } from "@angular/router";
import { AsyncPipe } from '@angular/common';
import { PlayerSearchResultItem, TeamSearchResultItem } from '../models/most-searched-models/most-searched-items';

@Component({
  selector: 'app-search-page',
  imports: [OverlayModule, AsyncPipe, ReactiveFormsModule, SearchBar, RouterLink],
  templateUrl: './search-page.html',
  styleUrl: './search-page.css',
})
export class SearchPage {
  overlayOpen = signal(false);
  searchTerm = signal('');
  hasSearched = signal(false);
  currentSearchTerm = signal('');
  searchResultsData = signal<SearchTermsData>({
    search_results: [
      {
        field: 'Players Results',
        players_data: [] as PlayerSearchResultItem[],
      },
      {
        field: 'Teams Results',
        teams_data: [] as TeamSearchResultItem[],
      },
      {
        field: 'Competitions Results',
        competitions_data: [] as Competition[]
      }
    ]
  });
  readonly appService = inject(AppService);
  readonly mostSearchedItems$ = this.appService.getMostSearchedItems();

  onSearchResults(results: SearchTermsData): void {
    this.searchResultsData.set(results);
    this.hasSearched.set(true);
  }
  onSearchTermChange(term: string): void {
    this.currentSearchTerm.set(term);
  }
  hasPlayersData(item: any): item is { field: string, players_data: PlayerSearchResultItem[] } {
    return 'players_data' in item;
  }

  hasTeamsData(item: any): item is { field: string, teams_data: TeamSearchResultItem[] } {
    return 'teams_data' in item;
  }

  hasCompetitionsData(item: any): item is { field: string, competitions_data: Competition[] } {
    return 'competitions_data' in item;
  }

}
