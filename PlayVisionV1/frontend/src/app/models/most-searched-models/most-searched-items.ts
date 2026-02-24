export interface PlayerSearchResultItem{
    slug: string,
    pname: string,
    lastname: string,
    nationality_flag: string,
    position: string,
    team_name: string
}

export interface TeamSearchResultItem{
    slug: string,
    title: string,
    logo_url: string,
    national_league: string,
    country_flag_url: string,
}