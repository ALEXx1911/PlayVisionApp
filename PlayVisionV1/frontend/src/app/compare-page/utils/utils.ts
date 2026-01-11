import { signal } from "@angular/core";
import { Competition, PlayerDetails,TeamModel, SearchTermsData } from "../../models/app-models";

export const DEFAULT_SEARCH_RESULTS =  signal<SearchTermsData>({
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
  });

export const DEFAULT_PLAYER : PlayerDetails = {
    slug: '',
    pname: '',
    lastname: '',
    common_name: '',
    position: '',
    age: 0,
    foot: '',
    height: '',
    nationality: '',
    nationality_flag: '',
    team_dorsal: 0,
    team: {
        title: '',
        slug: '',
        stadium: '',
        logo_url: '',
        shortname: '',
        coach: '',
        preferred_formation: '',
    }
}