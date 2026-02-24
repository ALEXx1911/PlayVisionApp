export interface PlayersListWithFlag{
    player_slug: string,
    player_common_name: string,
    player_position: string,
    country_flag: string,
    matches_played: number,
    minutes_played: number,
    goals: number,
    assists: number,
    yellow_cards: number,
    red_cards: number,
    correct_passes_media: number,
    tackles: number,
    media: number,
}

export interface PlayerSlot{
    name: string,
    position: string,
    dorsal: number,
    media: number,
    team_name: string,
    team_logo_url: string,
}