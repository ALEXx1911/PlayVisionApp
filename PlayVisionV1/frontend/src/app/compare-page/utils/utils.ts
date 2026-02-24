import { signal } from "@angular/core";
import { Competition, PlayerDetails,TeamModel, SearchTermsData } from "../../models/app-models";
import { PlayerSearchResultItem, TeamSearchResultItem } from "../../models/most-searched-models/most-searched-items";

export const DEFAULT_SEARCH_RESULTS =  signal<SearchTermsData>({
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

export const DEFAULT_PLAYER : PlayerSearchResultItem = {
    slug: '',
    pname: '',
    lastname: '',
    position: '',
    nationality_flag: '',
    team_name: '',
}