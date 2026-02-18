import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, shareReplay } from 'rxjs';
import { CountriesDataFromAPI, HomeDataAPI, CompetitionMatchesFromAPI, CompetitionDataFromAPI, TeamDataFromAPI, PlayerDataFromAPI, MatchDataFromAPI, ToPlayMatchFromAPI, FinishedMatchFromAPI, MostSearchedItems, SearchTermsData, PlayerCompareDataFromAPI, MostSearchedPlayers,  } from '../../models/app-models';

@Injectable({
  providedIn: 'root',
})
export class AppService {
  private http = inject(HttpClient);
  private apiHost = 'http://localhost:80/playVision/api/v1/';

  private homeDataCache$?: Observable<HomeDataAPI>;
  getHomeData():Observable<HomeDataAPI>{
    if (!this.homeDataCache$) {
      this.homeDataCache$ = this.http.get<HomeDataAPI>(`${this.apiHost}home/`,{
        mode:"cors"
      }).pipe(shareReplay(1));
    }
    return this.homeDataCache$!;
  }
  
  private countriesDataCache$?: Observable<CountriesDataFromAPI>;
  getAllCompetitions():Observable<CountriesDataFromAPI>{
    if (!this.countriesDataCache$) {
      this.countriesDataCache$ = this.http.get<CountriesDataFromAPI>(`${this.apiHost}competitions/`,{
        mode: "cors",
      }).pipe(shareReplay(1));
    }
    return this.countriesDataCache$!;
  }
  private competitionDetailsCache = new Map<string, Observable<CompetitionDataFromAPI>>();
  getCompetitionDetails(competition:string):Observable<CompetitionDataFromAPI>{
    //const params = new HttpParams()
    //  .set("title",competition);
    if (!this.competitionDetailsCache.has(competition)) {
      const request$ = this.http.get<CompetitionDataFromAPI>(`${this.apiHost}competitions/${competition}`,{
        mode: "cors",
        //params
      }).pipe(shareReplay(1));
      this.competitionDetailsCache.set(competition, request$);
    }
    return this.competitionDetailsCache.get(competition)!;
  
  }

  private competitionMatchesCache = new Map<string, Observable<CompetitionMatchesFromAPI>>();
  getCompetitionMatches(competition:string,start:number,limit:number):Observable<CompetitionMatchesFromAPI>{
    let qparams = new HttpParams()
      .set("start", start.toString())
      .set("limit", limit.toString());
    if (!this.competitionMatchesCache.has(competition)) {
      const  request$ = this.http.get<CompetitionMatchesFromAPI>(`${this.apiHost}competitions/${competition}/matches`,{
        mode: "cors",
        params: qparams
      }).pipe(shareReplay(1));
      this.competitionMatchesCache.set(competition, request$);
    }
    return this.competitionMatchesCache.get(competition)!;
  }

  private teamCache = new Map<string, Observable<TeamDataFromAPI>>();

  getTeamDetails(teamName:string):Observable<TeamDataFromAPI>{
    const encodedTeamName = encodeURIComponent(teamName);
    
    if (!this.teamCache.has(encodedTeamName)) {
      const request$ = this.http.get<TeamDataFromAPI>(`${this.apiHost}teams/${encodedTeamName}`,{
        mode: "cors",
      }).pipe(shareReplay(1));
      this.teamCache.set(encodedTeamName, request$);
    }
    return this.teamCache.get(encodedTeamName)!;
  }

  getPlayerDetails(playerName:string):Observable<PlayerDataFromAPI>{
    const encodedPlayerName = encodeURIComponent(playerName);
    return this.http.get<PlayerDataFromAPI>(`${this.apiHost}players/${encodedPlayerName}`,{
      mode: "cors",
    });
  }

  private matchCache = new Map<number, Observable<MatchDataFromAPI>>();

  getMatchDetails(matchId:number):Observable<MatchDataFromAPI>{
    if (!this.matchCache.has(matchId)) {
      const encodedIdMatch = encodeURIComponent(matchId);
      const request$ = this.http.get<MatchDataFromAPI>(`${this.apiHost}matchs/${encodedIdMatch}`,{
        mode: "cors",
      }).pipe(shareReplay(1));
      this.matchCache.set(matchId, request$);
    }
    return this.matchCache.get(matchId)!;
  }

  private previewMatchCache = new Map<number, Observable<ToPlayMatchFromAPI>>();
  getPreviewMatchDetails(matchId:number):Observable<ToPlayMatchFromAPI>{
    const encodedIdMatch = encodeURIComponent(matchId);
    if (!this.previewMatchCache.has(matchId)) {
      const request$ = this.http.get<ToPlayMatchFromAPI>(`${this.apiHost}matchs/${encodedIdMatch}`,{
        mode: "cors",
      }).pipe(shareReplay(1));
      this.previewMatchCache.set(matchId, request$);
    }
    return this.previewMatchCache.get(matchId)!;
  }

  private finishedMatchCache = new Map<number, Observable<FinishedMatchFromAPI>>();

  getFinishedMatchDetails(matchId:number):Observable<FinishedMatchFromAPI>{
    if (!this.finishedMatchCache.has(matchId)) {
      const encodedIdMatch = encodeURIComponent(matchId);
      const request$ = this.http.get<FinishedMatchFromAPI>(`${this.apiHost}matchs/${encodedIdMatch}`,{
        mode: "cors",
      }).pipe(shareReplay(1));
      this.finishedMatchCache.set(matchId, request$);
    }
    return this.finishedMatchCache.get(matchId)!;
  }

  searchTerms(term: string): Observable<SearchTermsData> {
    const params = new HttpParams().set('searchTerm', term);
    return this.http.get<SearchTermsData>(`${this.apiHost}search/`, {
      params,
      mode: 'cors',
    });
  }

  getMostSearchedItems():Observable<MostSearchedItems>{
    return this.http.get<MostSearchedItems>(`${this.apiHost}mostsearched/items`,{
      mode: "cors",
    });
  }

  getMostSearchedPlayers():Observable<MostSearchedPlayers>{
    return this.http.get<MostSearchedPlayers>(`${this.apiHost}mostsearched/players`,{
      mode: "cors",
    });
  }

  getPlayerCompareData(player1Name?:string, player2Name?:string):Observable<PlayerCompareDataFromAPI>{
    let encodedPlayerName1;
    let encodedPlayerName2;
    let qparams = new HttpParams();

    if(player1Name !== undefined && player2Name !== undefined){
      encodedPlayerName1 = encodeURIComponent(player1Name);
      encodedPlayerName2 = encodeURIComponent(player2Name);
      qparams = qparams.set("player1", encodedPlayerName1);
      qparams = qparams.set("player2", encodedPlayerName2);
    }
    
    return this.http.get<PlayerCompareDataFromAPI>(`${this.apiHost}compare/players/`,{
      mode: "cors",
      params: qparams
    });
  }

}
