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
export interface TeamModel{
    title: string;
    slug: string;
    stadium: string;
    logo_url:string;
    shortname: string;
    coach: string;
    preferred_formation: string;
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

export interface HomeDataAPI{
    competitions: CompetitionMatches[],
    top_scorers: PlayerStat[],
    most_yellow_cards: PlayerStat[],
    top_media_players: PlayerStat[],
    top_goalkeepers: PlayerStat[],
    top_players_lineup: PlayerSlotLineup[],
}
