import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

@Injectable({
  providedIn: 'root',
})

export class RecentSearchService {
    private readonly storageKey = 'recentSearches';
    private maxItems = 5;

    private _bs = new BehaviorSubject<string[]>(this.loadFromStorage());
    recentSearches$ = this._bs.asObservable();

    constructor () {
        if (typeof window !== 'undefined') {
            const data = window.localStorage.getItem(this.storageKey);
            if (data) {
                this._bs.next(JSON.parse(data));
            }

        }
    }

    private loadFromStorage(): string[] {
        try {
            if (typeof window === 'undefined') return [];

            const data = window.localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : [];    
        } catch {
            return [];
        }
    }

    private saveSearchesToStorage(searches: string[]): void {
        try {
            if (typeof window !== 'undefined') localStorage.setItem(this.storageKey, JSON.stringify(searches));
        }catch {}
        this._bs.next(searches);
    }

    addRecentSearch(search: string): void {
        const searchTerm = search?.trim();
        if (!searchTerm) return;

        const currentSearch = this._bs.getValue();
        const filteredSearch = currentSearch.filter(search => search.toLowerCase() !== searchTerm.toLowerCase());
    
        //Add the new search tearm to the start of the array
        filteredSearch.unshift(searchTerm);

        if (filteredSearch.length > this.maxItems) {
            filteredSearch.splice(this.maxItems);
        }
        this.saveSearchesToStorage(filteredSearch);

    }

    deleteRecentSearch(search: string): void {
        const currentSearch = this._bs.getValue();
        const updatedSearch = currentSearch.filter(item => item.toLowerCase() !== search.toLowerCase());
        this.saveSearchesToStorage(updatedSearch);
    }

    clearRecentSearches(): void {
        this.saveSearchesToStorage([]);
    }

}