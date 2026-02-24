import { PlayerSearchResultItem, TeamSearchResultItem } from "./most-searched-models/most-searched-items";
import { MostYellowCardData, TopGoalkeeperData, TopMediaPlayerData, TopScorersData } from "./player-models/player-models";
import { PlayersListWithFlag } from "./team-models/team-models";

export interface Player{
    pname: string,
    lastname: string,
    position: string,
    common_name: string,
    slug: string,
    team_dorsal: number,
    nationality_flag: string,
    team_name: string,
    team_logo_url: string,
}

export interface PlayerStatBasic{
    id: number,
    matches_played: number,
    minutes_played: number,
    goals: number,
    head_goals: number,
    penalty_goals: number,
    freekikgoals: number,
    assists: number,
    yellow_cards: number,
    red_cards: number,
    correctpassesmedia: number,
    cleansheets: number,
    tackles: number,
    media: number,
}

export interface TeamModel{
    title: string;
    slug: string;
    stadium: string;
    logo_url:string;
    shortname: string;
    coach: string;
    preferred_formation: string;
}

export interface TeamDataFromAPI{
    team: TeamModel,
    insights: TeamInsights[],
    player_stats: PlayersListWithFlag[],
    team_lineup: PlayerSlotLineup[],
    matches: Match[],
    last_five_results: string[],
}

export interface TeamInsights{
    insight_type: string,
    title: string,
    category: string,
    description: string,
}

export interface TeamCompetitionStat{
    team: TeamModel
    matches_played: number,
    win: number,
    draw: number,
    lose: number,
    goals_for: number,
    goals_against: number,
    goal_difference: number,
    point: number,
}

export interface Competition{
    id: number
    title: string,
    slug: string,
    country: string,
    competition_type: string,
    logo_url: string
}

export interface CompetitionShort{
    title: string,
    logo_url: string,
}

export interface Match{
    id: number,
    match_date: string,
    start_time: string,
    home_goals: number,
    away_goals: number,
    stadium: string,
    status: string,
    description: string,
    home_team: TeamModel,
    away_team: TeamModel,
    competition: CompetitionShort,
}

export interface MatchDataFromAPI{
    match_data: Match,
    home_team: TeamCompetitionStat,
    away_team: TeamCompetitionStat,
    home_last_matches: Match[],
    away_last_matches: Match[],
}

export interface MatchEvent{
    event_type: string,
    minute: number,
    description: string,
    player_name: Player,
    assist_player: Player,
    out_player: Player,
}

export interface MatchStat{
    field: string,
    home_data: number,
    away_data: number,
}

export interface ToPlayMatchFromAPI{
    match_data: Match,
    home_team_stats: TeamCompetitionStat,
    away_team_stats: TeamCompetitionStat,
    home_last_matches: Match[],
    away_last_matches: Match[],
}

export interface FinishedMatchFromAPI{
    match_data: Match,
    match_events: MatchEvent[],
    match_stats: MatchStat[],
}

export interface PlayerDetails{
    slug: string,
    pname: string,
    lastname: string,
    common_name: string,
    position: string,
    age: number,
    foot: string,
    height: string,
    nationality: string,
    nationality_flag: string,
    team_dorsal: number,
    team: TeamModel,
}

export interface PlayerStat{
    id: number,
    matches_played: number,
    minutes_played: number,
    goals: number,
    head_goals: number,
    penalty_goals: number,
    freekikgoals: number,
    assists: number,
    yellow_cards: number,
    red_cards: number,
    correctpassesmedia: number,
    cleansheets: number,
    tackles: number,
    media: number,
    player: Player
}

export interface PlayerDataFromAPI{
    player_data: PlayerDetails,
    competition_stats: PlayerStat[],
    season_stats: PlayerStat[],
}

export interface PlayerSlotLineup{
    pname: string,
    position: string,
    dorsal: number,
    media: number,
    team_name: string,
    team_logo_url: string,
}

export interface CompetitionMatches {
    id: number,
    title: string,
    slug: string,
    country_logo_url: string,
    country: string,
    competition_matches: Match[]
}
export interface CompetitionMatchesFromAPI{
    matches: Match[],
    total_matches: number,
}

export interface CompetitionDataFromAPI{
    competition_data:Competition,
    team_competition_stats: TeamCompetitionStat[],
    top_scorers: TopScorersData[],
    most_yellow_cards: MostYellowCardData[],
    top_media_players: TopMediaPlayerData[],
    top_goalkeepers: TopGoalkeeperData[],
}

export interface HomeDataAPI{
    competitions: CompetitionMatches[],
    top_scorers: TopScorersData[],
    most_yellow_cards: MostYellowCardData[],
    top_media_players: TopMediaPlayerData[],
    top_goalkeepers: TopGoalkeeperData[],
    top_players_lineup: PlayerSlotLineup[],
}

export interface Country{
    id: number,
    country_name: string,
    flag_url: string,
    competitions: Competition[],
}

export interface CountriesDataFromAPI{
    countries: Country[],
}

export interface SearchTermsData{
    search_results: [
        {
            field: string,
            players_data: PlayerSearchResultItem[]
        },
        {
            field: string,
            teams_data: TeamSearchResultItem[]
        },
        {
            field: string,
            competitions_data: Competition[]
        }
    ]
}

export interface PlayerCompareDataFromAPI{
    player1_data: PlayerDetails,
    player1_season_stats: PlayerStatBasic,
    player2_data: PlayerDetails,
    player2_season_stats: PlayerStatBasic,
}

export interface MostSearchedItems{
    most_searched_players: PlayerSearchResultItem[],
    most_searched_teams:  TeamSearchResultItem[],
    most_searched_competitions: Competition[],
}

export interface MostSearchedPlayers{
    most_searched_players: PlayerSearchResultItem[],
}