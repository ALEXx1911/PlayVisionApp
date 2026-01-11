import { Component, EventEmitter, inject, Input, input, Output, signal } from "@angular/core";
import { RecentSearchService } from "../../services/recent-search.service";
import { AppService } from "../../../services/app-service";
import { FormControl, ReactiveFormsModule } from "@angular/forms";
import { catchError, filter, map, of, shareReplay, startWith, Subject, switchMap, tap, withLatestFrom } from "rxjs";
import { Competition, PlayerDetails, SearchTermsData, TeamModel } from "../../../models/app-models";
import { MatIcon } from "@angular/material/icon";
import { MatDivider } from "@angular/material/divider";
import { MatActionList, MatListItem } from "@angular/material/list";
import { AsyncPipe } from "@angular/common";
import { OverlayModule } from "@angular/cdk/overlay";
import { toSignal } from "@angular/core/rxjs-interop";

@Component({
    selector: 'app-search-bar',
    imports: [MatIcon, OverlayModule, AsyncPipe, ReactiveFormsModule, MatDivider, MatActionList, MatListItem],
    templateUrl: './search-bar.html',
})
export class SearchBar {
    isSearchPage = input(false);
    overlayOpen = signal(false);
    searchTerm = signal('');
    readonly searchService = inject(AppService);
    fc = new FormControl('');
    confirm$ = new Subject<void>();
    readonly recentSearchService = inject(RecentSearchService);
    @Input({ required: false }) selectPlayerForComparison?: (player: PlayerDetails) => void;
    @Output() searchResults = new EventEmitter<SearchTermsData>();
    @Output() searchTermChange = new EventEmitter<string>();
    
    recentSearchesData$ = this.recentSearchService.recentSearches$;
    searchResultsData$ = this.confirm$.pipe(
        withLatestFrom(this.fc.valueChanges.pipe(startWith(''))),
        map(([_, term]) => (term ?? '').trim()),
        filter(term => term.length > 0),
        switchMap(term => 
          this.searchService.searchTerms(term).pipe(
            tap((r) => {
              this.recentSearchService.addRecentSearch(term);
              this.overlayOpen.set(false);
              this.searchResults.emit(r);
              this.searchTermChange.emit(term);
            }),
            catchError(() => {
              const emptyResults: SearchTermsData = {
                search_results: [
                  {
                    field: 'Players Results',
                    players_data: [] as PlayerDetails[],
                  },
                  {
                    field: 'Teams Results',
                    teams_data: [] as TeamModel[],
                  },
                  {
                    field: 'Competitions Results',
                    competitions_data: [] as Competition[]
                  }
                ]
              };
              this.searchResults.emit(emptyResults);
              this.searchTermChange.emit(term);
              return of(emptyResults);
            })
          )
        ), 
        shareReplay(1)
      );

  searchResults_signal = toSignal(this.searchResultsData$,  { initialValue: null });

  confirmSearch(): void {
    this.confirm$.next();
  }

  clearSearch(): void {
    this.fc.setValue('');
    this.searchTerm.set('');
  }
  useRecentSearch(term: string): void {
    this.fc.setValue(term);
    this.searchTerm.set(term);
    this.confirmSearch();
  }

  deleteRecentSearch(search: string): void {
    this.recentSearchService.deleteRecentSearch(search);
  }

  hasPlayersData(item: any): item is { field: string, players_data: PlayerDetails[] } {
    return 'players_data' in item;
  }

  hasTeamsData(item: any): item is { field: string, teams_data: TeamModel[] } {
    return 'teams_data' in item;
  }

  hasCompetitionsData(item: any): item is { field: string, competitions_data: Competition[] } {
    return 'competitions_data' in item;
  }
}