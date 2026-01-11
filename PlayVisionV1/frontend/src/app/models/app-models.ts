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
    player_stats: PlayerStat[],
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
    team_competition_stats: TeamCompetitionStat[]
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
    logo_url: string,
    country: string,
    competition_matches: Match[]
}
export interface CompetitionMatchesFromAPI{
    matches: Match[],
    total_matches: number,
}

export interface DataFromCompetitionAPI{
    competition:Competition,
    top_scorers: PlayerStat[],
    most_yellow_cards: PlayerStat[],
    top_media_players: PlayerStat[],
    top_goalkeepers: PlayerStat[],
}

export interface HomeDataAPI{
    competitions: CompetitionMatches[],
    top_scorers: PlayerStat[],
    most_yellow_cards: PlayerStat[],
    top_media_players: PlayerStat[],
    top_goalkeepers: PlayerStat[],
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