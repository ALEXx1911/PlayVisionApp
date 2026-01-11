import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, shareReplay } from 'rxjs';
import { CountriesDataFromAPI, HomeDataAPI } from '../models/app-models';

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
}
