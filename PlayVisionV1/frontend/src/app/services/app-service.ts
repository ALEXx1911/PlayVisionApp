import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, shareReplay } from 'rxjs';
import { CountriesDataFromAPI, HomeDataAPI, CompetitionMatchesFromAPI, DataFromCompetitionAPI, TeamDataFromAPI, PlayerDataFromAPI, MatchDataFromAPI, ToPlayMatchFromAPI, FinishedMatchFromAPI,  } from '../models/app-models';

@Injectable({
  providedIn: 'root',
})
export class AppService {
  private http = inject(HttpClient);
  private apiHost = 'http://localhost:80/playVision/api/';

  getHomeData():Observable<HomeDataAPI>{
    return this.http.get<HomeDataAPI>(`${this.apiHost}home/`,{
      mode:"cors"
    });
  }
  
  getAllCompetitions():Observable<CountriesDataFromAPI>{
    return this.http.get<CountriesDataFromAPI>(`${this.apiHost}competitions/`,{
      mode: "cors",
    });
  }
  
  getCompetitionDetails(competition:string):Observable<DataFromCompetitionAPI>{
    //const params = new HttpParams()
    //  .set("title",competition);
    return this.http.get<DataFromCompetitionAPI>(`${this.apiHost}competitions/${competition}`,{
      mode: "cors",
      //params
    })
  }

  getCompetitionMatches(competition:string,start:number,limit:number):Observable<CompetitionMatchesFromAPI>{
    let qparams = new HttpParams()
      .set("start", start.toString())
      .set("limit", limit.toString());
    return this.http.get<CompetitionMatchesFromAPI>(`${this.apiHost}competitions/${competition}/matches`,{
      mode: "cors",
      params: qparams
    });
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

  getMatchDetails(matchId:number):Observable<MatchDataFromAPI>{
    const encodedIdMatch = encodeURIComponent(matchId);
    return this.http.get<MatchDataFromAPI>(`${this.apiHost}matchs/${encodedIdMatch}`,{
    mode: "cors",
    });
  }

  getPreviewMatchDetails(matchId:number):Observable<ToPlayMatchFromAPI>{
    const encodedIdMatch = encodeURIComponent(matchId);
    return this.http.get<ToPlayMatchFromAPI>(`${this.apiHost}matchs/${encodedIdMatch}`,{
    mode: "cors",
    });
  }

  getFinishedMatchDetails(matchId:number):Observable<FinishedMatchFromAPI>{
    const encodedIdMatch = encodeURIComponent(matchId);
    return this.http.get<FinishedMatchFromAPI>(`${this.apiHost}matchs/${encodedIdMatch}`,{
    mode: "cors",
    });
  }

}
