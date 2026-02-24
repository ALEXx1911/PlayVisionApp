import { Component, effect, EventEmitter, inject, Input, input, Output, signal } from "@angular/core";
import { RecentSearchService } from "../../services/recent-search.service";
import { AppService } from "../../../services/app-services/app-service";
import { Competition, SearchTermsData} from "../../../models/app-models";
import { MatIcon } from "@angular/material/icon";
import { MatDivider } from "@angular/material/divider";
import { MatActionList, MatListItem } from "@angular/material/list";
import { OverlayModule } from "@angular/cdk/overlay";
import { toSignal } from "@angular/core/rxjs-interop";
import { PlayerSearchResultItem, TeamSearchResultItem } from "../../../models/most-searched-models/most-searched-items";

@Component({
    selector: 'app-search-bar',
    imports: [MatIcon, OverlayModule, MatDivider, MatActionList, MatListItem],
    templateUrl: './search-bar.html',
})
export class SearchBar {
    isSearchPage = input(false);
    overlayOpen = signal(false);
    searchInput = signal('');
    shouldSearch = signal(false);
    searchResultsData = signal<SearchTermsData | null>(null);
    readonly searchService = inject(AppService);
    readonly recentSearchService = inject(RecentSearchService);
    @Input({ required: false }) selectPlayerForComparison?: (player: PlayerSearchResultItem) => void;
    @Output() searchResults = new EventEmitter<SearchTermsData>();
    @Output() searchTermChange = new EventEmitter<string>();
    
    recentSearchesData = toSignal(this.recentSearchService.recentSearches$, { initialValue: [] });
    
      constructor() {
        effect(() => {
          if(!this.shouldSearch()){
            return;
          }
          const term = this.searchInput();

          if(!term || term.trim().length === 0){
            return;
          }

          this.shouldSearch.set(false);

          this.searchService.searchTerms(term).subscribe({
            next: (results) => {
              this.recentSearchService.addRecentSearch(term);
              this.overlayOpen.set(false);

              this.searchResultsData.set(results);
              this.searchResults.emit(results);
              this.searchTermChange.emit(term);
              this.shouldSearch.set(false);
            },
            error: () => {
              const emptyResults: SearchTermsData = {
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
              }
            }
          })
        });
      }


  //searchResults_signal = toSignal(this.searchResultsData$,  { initialValue: null });

  confirmSearch(): void {
    this.shouldSearch.set(true);
  }

  clearSearch(): void {
    this.searchInput.set('');
  }
  useRecentSearch(term: string): void {
    this.searchInput.set(term);
    this.confirmSearch();
  }

  deleteRecentSearch(search: string): void {
    this.recentSearchService.deleteRecentSearch(search);
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