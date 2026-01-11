import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, shareReplay } from 'rxjs';
import { CountriesDataFromAPI, HomeDataAPI, CompetitionMatchesFromAPI, DataFromCompetitionAPI } from '../models/app-models';

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
}
