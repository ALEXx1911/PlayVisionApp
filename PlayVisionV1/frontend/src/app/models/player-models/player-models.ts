import { Player } from "../app-models";

export interface TopScorersData{
    player : Player,
    goals: number,
    freekick_goals: number,
    penalty_goals: number,
    head_goals: number,
    matches_played: number,
    minutes_played: number,
    media: number,
}

export interface TopMediaPlayerData{
    player: Player,
    media: number,
    matches_played: number,
    minutes_played: number,
    goals: number,
    assists: number,
    correct_passes_media: number,
}

export interface MostYellowCardData{
    player: Player,
    matches_played: number,
    tackles: number,
    yellow_cards: number,
}

export interface TopGoalkeeperData{
    player: Player,
    matches_played: number,
    minutes_played: number,
    yellow_cards: number,
    cleansheets: number,
}