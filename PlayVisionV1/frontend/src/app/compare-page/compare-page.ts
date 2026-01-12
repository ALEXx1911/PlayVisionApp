import { Component, computed, inject, Signal, signal } from '@angular/core';
import { SearchBar } from "../search-page/components/search-bar/search-bar";
import { AppService } from '../services/app-services/app-service';
import { PlayerDetails, SearchTermsData } from '../models/app-models';
import { DEFAULT_PLAYER, DEFAULT_SEARCH_RESULTS } from './utils/utils';
import { AsyncPipe } from '@angular/common';
import { MatIcon } from "@angular/material/icon";
import { CompareResults } from "./compare-results/compare-results";

@Component({
  selector: 'app-compare-page',
  imports: [SearchBar, AsyncPipe, MatIcon, CompareResults],
  templateUrl: './compare-page.html',
  styleUrl: './compare-page.css',
})
export class ComparePage {
  readonly appService = inject(AppService);
  readonly mostSearchedPlayers$ = this.appService.getMostSearchedPlayers();
  
  isSubmited = signal(false);
  hasSearched = signal(false);
  currentSearchTerm = signal('');
  player1 = signal<PlayerDetails>(DEFAULT_PLAYER);
  player2 = signal<PlayerDetails>(DEFAULT_PLAYER);
  
  player1Selected = signal(false);
  player2Selected = signal(false);
  isBothPlayersSelected:Signal<boolean> = computed(
  () => this.player1Selected() && this.player2Selected());
  
  searchResultsData = DEFAULT_SEARCH_RESULTS;

  onSearchResults(results: SearchTermsData): void {
    this.searchResultsData.set(results);
    this.hasSearched.set(true);
  }
  onSearchTermChange(term: string): void {
    this.currentSearchTerm.set(term);
  }

  selectPlayerForComparison(player: PlayerDetails): void {
    if (!this.player1Selected()) {
      this.player1.set(player);
      this.player1Selected.set(true);
    } else if (!this.player2Selected() && player.pname !== this.player1().pname) {
      this.player2.set(player);
      this.player2Selected.set(true);
    }
  }

  deselectPlayer(playerNumber: number): void {
    if (playerNumber === 1) {
      this.player1.set(DEFAULT_PLAYER);
      this.player1Selected.set(false);
    } else if (playerNumber === 2) {
      this.player2.set(DEFAULT_PLAYER);
      this.player2Selected.set(false);
    }
  }

  compareSelectedPlayers(): void {
    if (this.player1Selected() && this.player2Selected()) {
      this.isSubmited.set(true);
    }
  }

  hasPlayersData(item: any): item is { field: string, players_data: PlayerDetails[] } {
    return 'players_data' in item;
  }
}
