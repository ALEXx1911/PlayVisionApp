import { signal } from "@angular/core";

export type PlayerAnalysisMessage = {
    key: string;
    message: string;
};

export const DEFAULT_MESSAGES_TO_ANALIZE_DATA = signal<PlayerAnalysisMessage[]>([
    {
        key: 'Goalkeeper Stats',
        message: 'When analyzing goalkeepers, the focus should be on shot-stopping ability and reliability and clean sheets'
    },
    {
        key: 'Defender Stats',
        message: 'For defenders, defensive consistency and positioning are essential. Important statistics include tackles won, interceptions.It is also useful to consider passing accuracy to evaluate their contribution to ball progression'
    },
    {
        key: 'Winger Stats',
        message: 'Wingers require a balance between defense and attack. Relevant statistics include crosses completed, assists, key passes, and dribbles, alongside defensive actions such as tackles and recoveries'
    },
    {
        key: 'Midfielder Stats',
        message: 'Midfield analysis should focus on control, creativity, and work rate.Key metrics include passes completed, pass accuracy, chances created, and ball recoveries'
    },
    {
        key: 'Forward Stats',
        message: 'For forwards, the main focus is efficiency in scoring and attacking contribution. Important statistics include goals, shots on target, conversion rate, and assists'
    }
]);
    